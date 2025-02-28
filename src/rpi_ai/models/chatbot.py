from collections.abc import Callable
from typing import ClassVar

from google.genai import Client
from google.genai.errors import ServerError
from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
    GoogleSearchRetrieval,
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
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class Chatbot:
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

    def __init__(self, api_key: str, config: ChatbotConfig, functions: list[Callable]) -> None:
        self._client = Client(api_key=api_key)
        self._config = config
        self._functions = [*functions, self.web_search]
        self._history: list[Message] = []
        self.start_chat()

    @property
    def _model_config(self) -> GenerateContentConfig:
        return GenerateContentConfig(
            system_instruction=self._config.system_instruction,
            max_output_tokens=self._config.max_output_tokens,
            temperature=self._config.temperature,
            safety_settings=self.SAFETY_SETTINGS,
            candidate_count=1,
        )

    @property
    def _chat_config(self) -> GenerateContentConfig:
        _config = self._model_config
        _config.tools = self._functions
        return _config

    @property
    def _web_search_config(self) -> GenerateContentConfig:
        _config = self._model_config
        _config.tools = [Tool(google_search=GoogleSearchRetrieval)]
        return _config

    @property
    def chat_history(self) -> MessageList:
        return MessageList(self._history)

    def web_search(self, query: str) -> str:
        """
        Search the web for the given query.

        Args:
            query (str): The search query.

        Returns:
            str: The search results.
        """
        response = self._client.models.generate_content(
            contents=query,
            model=self._config.model,
            config=self._web_search_config,
        )
        return response.text

    def _extract_blocked_categories(self, response: GenerateContentResponse) -> list[str]:
        blocked_categories = []
        for safety_rating in response.candidates[0].safety_ratings:
            if safety_rating.blocked:
                blocked_categories.extend(safety_rating.category)
        return blocked_categories

    def _handle_blocked_message(self, blocked_categories: list[str]) -> str:
        error_message = f"The previous message was blocked because it violates the following categories: {', '.join(blocked_categories)}."
        response = self._chat.send_message(error_message)
        reply = response.text
        self._history.append(Message.model_message(reply))
        return reply

    def get_config(self) -> ChatbotConfig:
        return self._config

    def update_config(self, config: ChatbotConfig) -> None:
        self._config = config

    def start_chat(self) -> None:
        self._history = [Message.new_chat_message()]
        self._chat = self._client.chats.create(
            model=self._config.model,
            config=self._chat_config,
            history=self.chat_history.as_contents_list,
        )

    def send_message(self, text: str) -> Message:
        try:
            response = self._chat.send_message(text)
            self._history.append(Message.user_message(text))
            self._history.append(Message.model_message(response.text))
            return Message(message=response.text)
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send message to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                reply = self._handle_blocked_message(blocked_categories)
            else:
                self._history.pop()
                reply = "Failed to send message to chatbot!"

            return Message(message=reply)
        except ServerError:
            return Message(message="Model overloaded! Please try again.")

    def send_audio(self, audio_data: bytes) -> SpeechResponse:
        try:
            audio_request = audiobot.get_audio_request(audio_data)
            response = self._chat.send_message(audio_request)
            reply = response.text
            audio = audiobot.get_audio_bytes_from_text(reply.replace("*", ""))
            self._history.append(Message.user_message(audio_request[0]))
            self._history.append(Message.model_message(reply))
            return SpeechResponse(bytes=audio, message=reply)
        except (AttributeError, ValidationError) as e:
            msg = f"Failed to send audio to chatbot: {e}"
            logger.exception(msg)

            if blocked_categories := self._extract_blocked_categories(response):
                reply = self._handle_blocked_message(blocked_categories)
            else:
                self._history.pop()
                reply = "Failed to send audio to chatbot!"

            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply)
        except ServerError:
            reply = "Model overloaded! Please try again."
            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply)
        except gTTSError as e:
            msg = f"A gTTSError occurred: {e}"
            logger.exception(msg)
            return SpeechResponse(bytes="", message=str(e))
