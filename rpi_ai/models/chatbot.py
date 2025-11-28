"""Chatbot implementation for the RPi AI application."""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any, ClassVar

from google.genai import Client
from google.genai.errors import ServerError
from google.genai.types import (
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

from rpi_ai.api_types import Message, MessageList, SpeechResponse
from rpi_ai.config import ChatbotConfig
from rpi_ai.models import audiobot

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

    def __init__(self, api_key: str, config: ChatbotConfig, functions: list[Callable[..., Any]]) -> None:
        """Initialize the chatbot with API key, configuration, and functions.

        :param str api_key:
            Google AI API key
        :param ChatbotConfig config:
            Chatbot configuration
        :param list[Callable[..., Any]] functions:
            List of available functions
        """
        self._client = Client(api_key=api_key)
        self._config = config
        self._functions: list[Tool | Callable[..., Any]] = [*functions, self.web_search]
        self._history: list[Message] = []
        self.start_chat()

    @property
    def _model_config(self) -> GenerateContentConfig:
        """Get base model configuration.

        :return GenerateContentConfig:
            Model configuration
        """
        return GenerateContentConfig(
            system_instruction=self._config.system_instruction,
            max_output_tokens=self._config.max_output_tokens,
            temperature=self._config.temperature,
            safety_settings=self.SAFETY_SETTINGS,
            candidate_count=self.CANDIDATE_COUNT,
        )

    @property
    def _chat_config(self) -> GenerateContentConfig:
        """Get chat configuration with functions.

        :return GenerateContentConfig:
            Chat configuration
        """
        _config = self._model_config
        _config.tools = self._functions
        return _config

    @property
    def _web_search_config(self) -> GenerateContentConfig:
        """Get web search configuration.

        :return GenerateContentConfig:
            Web search configuration
        """
        _config = self._model_config
        _config.tools = [Tool(google_search=GoogleSearch())]  # type: ignore[arg-type]
        return _config

    @property
    def chat_history(self) -> MessageList:
        """Get chat history as MessageList.

        :return MessageList:
            Current chat history
        """
        return MessageList(self._history)

    def web_search(self, query: str) -> str:
        """Search the web for the given query.

        :param str query:
            The search query
        :return str:
            The search results
        """
        response = self._client.models.generate_content(
            contents=query,
            model=self._config.model,
            config=self._web_search_config,
        )
        return response.text or ""

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
        error_message = f"The previous message was blocked because it violates the following categories: {', '.join(blocked_categories)}."
        response = self._chat.send_message(error_message)
        reply = response.text or "Unable to process blocked message."
        self._history.append(Message.model_message(reply, int(datetime.now().timestamp())))
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
        self._history = [Message.new_chat_message(int(datetime.now().timestamp()))]
        self._chat = self._client.chats.create(
            model=self._config.model,
            config=self._chat_config,
        )

    def send_message(self, text: str) -> Message:
        """Send a text message to the chatbot.

        :param str text:
            Message text to send
        :return Message:
            Chatbot response message
        """
        try:
            user_message = Message.user_message(text, int(datetime.now().timestamp()))
            self._history.append(user_message)

            response = self._chat.send_message(text)
            model_message = Message.model_message(response.text, int(datetime.now().timestamp()))
            self._history.append(model_message)
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send message to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                reply = self._handle_blocked_message(blocked_categories)
            else:
                self._history.pop()
                reply = "Failed to send message to chatbot!"

            return Message(message=reply, timestamp=int(datetime.now().timestamp()))
        except ServerError:
            self._history.pop()
            return Message(message="Model overloaded! Please try again.", timestamp=int(datetime.now().timestamp()))
        else:
            return model_message

    def send_audio(self, audio_data: bytes) -> SpeechResponse:
        """Send audio data to the chatbot and get speech response.

        :param bytes audio_data:
            Audio data to send
        :return SpeechResponse:
            Speech response with audio and text
        """
        try:
            audio_request = audiobot.get_audio_request(audio_data)
            user_message = Message.user_message(audio_request[0], int(datetime.now().timestamp()))
            self._history.append(user_message)

            response = self._chat.send_message(audio_request)
            model_message = Message.model_message(response.text, int(datetime.now().timestamp()))
            self._history.append(model_message)

            audio = audiobot.get_audio_bytes_from_text(response.text)
            return SpeechResponse(bytes=audio, message=response.text, timestamp=int(datetime.now().timestamp()))
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send audio to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                reply = self._handle_blocked_message(blocked_categories)
            else:
                self._history.pop()
                reply = "Failed to send audio to chatbot!"

            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply, timestamp=int(datetime.now().timestamp()))
        except ServerError:
            self._history.pop()
            reply = "Model overloaded! Please try again."
            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply, timestamp=int(datetime.now().timestamp()))
        except gTTSError as e:
            self._history.pop()
            self._history.pop()
            msg = f"A gTTSError occurred: {e}"
            logger.exception(msg)
            return SpeechResponse(bytes="", message=str(e), timestamp=int(datetime.now().timestamp()))
