"""Chatbot implementation for the RPi AI application."""

import logging
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar

import numpy as np
from google.genai import Client
from google.genai.errors import ServerError
from google.genai.types import (
    EmbedContentConfig,
    GenerateContentConfig,
    GenerateContentResponse,
    GoogleSearch,
    HarmBlockThreshold,
    HarmCategory,
    SafetySetting,
    Tool,
)
from gtts import gTTSError
from pydantic import ValidationError
from python_template_server.models import BaseResponse

from rpi_ai import audiobot
from rpi_ai.models import (
    ChatbotConfig,
    ChatbotMessage,
    ChatbotMessageList,
    ChatbotSpeech,
    ChatMemoryList,
    EmbeddingConfig,
)

logger = logging.getLogger(__name__)


class Chatbot:
    """Chatbot for handling AI conversations and audio interactions."""

    SAFETY_CATEGORIES: ClassVar[list[HarmCategory]] = [
        HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        HarmCategory.HARM_CATEGORY_HARASSMENT,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    ]

    SAFETY_SETTINGS: ClassVar[list[SafetySetting]] = [
        SafetySetting(category=category, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH) for category in SAFETY_CATEGORIES
    ]

    CANDIDATE_COUNT: int = 1

    def __init__(
        self,
        api_key: str,
        config_dir: Path,
        config: ChatbotConfig,
        embedding_config: EmbeddingConfig,
        functions: list[Callable[..., Any]],
        memories: ChatMemoryList | None = None,
    ) -> None:
        """Initialise the chatbot with API key, configuration, and functions.

        :param str api_key:
            Google AI API key
        :param ChatbotConfig config:
            Chatbot configuration
        :param EmbeddingConfig embedding_config:
            Embedding configuration
        :param list[Callable[..., Any]] functions:
            List of available functions
        :param ChatMemoryList | None memories:
            Optional pre-loaded chat memories
        """
        self._client = Client(api_key=api_key)
        self._config_dir = config_dir
        self._config = config
        self._embedding_config = embedding_config
        self._functions: list[Tool | Callable[..., Any]] = [
            *functions,
            self.create_memory,
            self.retrieve_memories,
            self.clear_memories,
            self.web_search,
        ]

        self._history: list[ChatbotMessage] = []

        self._memory = memories or ChatMemoryList.load_from_file(
            self._config_dir / self._embedding_config.memory_filepath
        )
        logger.info("Loaded %d memory entries.", len(self._memory.entries))
        self.start_chat()

    @property
    def _model_config(self) -> GenerateContentConfig:
        """Get base model configuration."""
        return GenerateContentConfig(
            system_instruction=f"{self._config.system_instruction}\n{ChatbotConfig.get_memory_guidelines()}",
            max_output_tokens=self._config.max_output_tokens,
            temperature=self._config.temperature,
            safety_settings=self.SAFETY_SETTINGS,
            candidate_count=self.CANDIDATE_COUNT,
        )

    @property
    def _chat_config(self) -> GenerateContentConfig:
        """Get chat configuration with functions."""
        _config = self._model_config
        _config.tools = self._functions
        return _config

    @property
    def _web_search_config(self) -> GenerateContentConfig:
        """Get web search configuration."""
        _config = self._model_config
        _config.tools = [Tool(google_search=GoogleSearch())]
        return _config

    @property
    def chat_history(self) -> ChatbotMessageList:
        """Get chat history as ChatbotMessageList."""
        return ChatbotMessageList(messages=self._history)

    def _get_current_timestamp(self) -> int:
        """Get the current timestamp.

        :return int:
            Current timestamp
        """
        timestamp_str = BaseResponse.current_timestamp()
        return int(datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")).timestamp())

    def _embed_text(self, text: str, task_type: str) -> np.ndarray:
        """Generate embedding for the given text.

        :param str text:
            Text to embed
        :param str task_type:
            Task type for embedding optimization
        :return np.ndarray:
            Embedding vector
        """
        embedding_response = self._client.models.embed_content(
            model=self._embedding_config.model,
            contents=text,
            config=EmbedContentConfig(task_type=task_type),
        )
        return np.array(embedding_response.embeddings[0].values)

    def create_memory(self, text: str) -> None:
        """Create a persistent chat memory.

        :param str text:
            Memory text to store
        """
        vector = self._embed_text(text, task_type="SEMANTIC_SIMILARITY")
        self._memory.add_entry(text=text, vector=vector.tolist(), max_memories=self._embedding_config.max_memories)
        self._memory.save_to_file(self._config_dir / self._embedding_config.memory_filepath)
        logger.info("Stored new memory (%d entries): %s", len(self._memory.entries), text)

    def retrieve_memories(self, query: str) -> list[str]:
        """Retrieve relevant memories based on the query.

        :param str query:
            Query text to find relevant memories
        :return list[str]:
            List of relevant memory texts
        """
        query_vector = self._embed_text(query, task_type="SEMANTIC_SIMILARITY")
        memories = self._memory.retrieve_memories(query_vector.tolist(), top_k=self._embedding_config.top_k)
        logger.info("Retrieved %d relevant memories for query: %s", len(memories), query)
        return memories

    def clear_memories(self) -> None:
        """Clear all stored chat memories."""
        self._memory.clear_entries()
        self._memory.save_to_file(self._config_dir / self._embedding_config.memory_filepath)
        logger.info("Cleared all chat memories.")

    def web_search(self, query: str) -> str:
        """Search the web for the given query.

        :param str query:
            The search query
        :return str:
            The search results
        """
        logger.info("Performing web search for query: %s", query)
        reply = self._client.models.generate_content(
            contents=query,
            model=self._config.model,
            config=self._web_search_config,
        )
        return reply.text or ""

    def _extract_blocked_categories(self, response: GenerateContentResponse) -> list[str]:
        """Extract blocked safety categories from response.

        :param GenerateContentResponse response:
            Response to check for blocked categories
        :return list[str]:
            List of blocked category names
        """
        if not (response.candidates and response.candidates[0].safety_ratings):
            return []

        return [
            str(safety_rating.category)
            for safety_rating in response.candidates[0].safety_ratings
            if safety_rating.blocked and safety_rating.category
        ]

    def _handle_blocked_message(self, blocked_categories: list[str]) -> str:
        """Handle blocked message by generating error response.

        :param list[str] blocked_categories:
            List of blocked categories
        :return str:
            Error message response
        """
        blocked_categories_str = ", ".join(blocked_categories)
        response = self._chat.send_message(
            f"The previous message was blocked because it violates the following categories: {blocked_categories_str}."
        )
        reply = response.text or "Unable to process blocked message."
        self._history.append(ChatbotMessage.model_message(reply, self._get_current_timestamp()))
        return reply

    def get_config(self) -> ChatbotConfig:
        """Get current chatbot configuration.

        :return ChatbotConfig:
            Current configuration
        """
        return self._config

    def update_config(self, config: ChatbotConfig) -> None:
        """Update chatbot configuration.

        :param ChatbotConfig config:
            New configuration
        """
        self._config = config

    def start_chat(self) -> None:
        """Start a new chat session."""
        self._history = [ChatbotMessage.new_chat_message(self._get_current_timestamp())]
        self._chat = self._client.chats.create(
            model=self._config.model,
            config=self._chat_config,
        )

    def send_message(self, text: str) -> ChatbotMessage:
        """Send a text message to the chatbot.

        :param str text:
            ChatbotMessage text to send
        :return ChatbotMessage:
            Chatbot response message
        """
        try:
            user_message = ChatbotMessage.user_message(text, self._get_current_timestamp())

            response = self._chat.send_message(text)

            if not (response_text := response.text):
                msg = "No response text received from chatbot."
                logger.error(msg)
                raise AttributeError(msg)  # noqa: TRY301

            model_message = ChatbotMessage.model_message(response_text, self._get_current_timestamp())

            self._history.append(user_message)
            self._history.append(model_message)
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send message to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                self._history.append(user_message)
                reply = self._handle_blocked_message(blocked_categories)
            else:
                reply = "Failed to send message to chatbot!"

            return ChatbotMessage(message=reply, timestamp=self._get_current_timestamp())
        except ServerError:
            logger.exception("Model overloaded.")
            return ChatbotMessage(
                message="Model overloaded! Please try again.", timestamp=self._get_current_timestamp()
            )
        else:
            return model_message

    def send_audio(self, audio_data: bytes) -> ChatbotSpeech:
        """Send audio data to the chatbot and get speech response.

        :param bytes audio_data:
            Audio data to send
        :return ChatbotSpeech:
            Speech response with audio and text
        """
        try:
            audio_request = audiobot.get_audio_request(audio_data)
            user_message = ChatbotMessage.user_message(str(audio_request[0]), self._get_current_timestamp())

            response = self._chat.send_message(audio_request)
            if not (response_text := response.text):
                msg = "No response text received from chatbot."
                logger.error(msg)
                raise AttributeError(msg)  # noqa: TRY301

            model_message = ChatbotMessage.model_message(response_text, self._get_current_timestamp())

            audio = audiobot.get_audio_bytes_from_text(response_text)
            speech_response = ChatbotSpeech(bytes=audio, message=response_text, timestamp=self._get_current_timestamp())

            self._history.append(user_message)
            self._history.append(model_message)
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send audio to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                self._history.append(user_message)
                reply = self._handle_blocked_message(blocked_categories)
            else:
                reply = "Failed to send audio to chatbot!"

            audio = audiobot.get_audio_bytes_from_text(reply)
            return ChatbotSpeech(bytes=audio, message=reply, timestamp=self._get_current_timestamp())
        except ServerError:
            reply = "Model overloaded! Please try again."
            audio = audiobot.get_audio_bytes_from_text(reply)
            logger.exception("Model overloaded.")
            return ChatbotSpeech(bytes=audio, message=reply, timestamp=self._get_current_timestamp())
        except gTTSError as e:
            msg = f"A gTTSError occurred: {e}"
            logger.exception(msg)
            return ChatbotSpeech(bytes="", message=str(e), timestamp=self._get_current_timestamp())
        else:
            return speech_response
