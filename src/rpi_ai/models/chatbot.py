from collections.abc import Callable

from google.genai import Client
from google.genai.types import GenerateContentConfig, GoogleSearchRetrieval, Tool
from gtts import gTTSError
from pydantic import ValidationError

from rpi_ai.models import audiobot
from rpi_ai.types import AIConfigType, Message, SpeechResponse


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType, functions: list[Callable]) -> None:
        self._client = Client(api_key=api_key)
        self._config = config
        functions.append(self._web_search)
        self._functions = functions

    def _web_search_config(self) -> Tool:
        return GenerateContentConfig(
            system_instruction=self._config.system_instruction,
            candidate_count=self._config.candidate_count,
            max_output_tokens=self._config.max_output_tokens,
            temperature=self._config.temperature,
            tools=[Tool(google_search=GoogleSearchRetrieval)],
        )

    def _web_search(self, query: str) -> str:
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
            config=self._web_search_config(),
        )
        return response.text

    def get_config(self) -> AIConfigType:
        return self._config

    def update_config(self, config: AIConfigType) -> None:
        self._config = config

    def start_chat(self) -> Message:
        self._chat = self._client.chats.create(
            model=self._config.model,
            config=GenerateContentConfig(
                system_instruction=self._config.system_instruction,
                candidate_count=self._config.candidate_count,
                max_output_tokens=self._config.max_output_tokens,
                temperature=self._config.temperature,
                tools=self._functions,
            ),
        )
        return Message(message="What's on your mind today?")

    def send_message(self, text: str) -> Message:
        try:
            response = self._chat.send_message(text)
            return Message(message=response.text)
        except (AttributeError, ValidationError):
            return Message(message="An error occurred! Please try again.")

    def send_audio(self, audio_data: bytes) -> SpeechResponse:
        try:
            audio_request = audiobot.get_audio_request(audio_data)
            response = self._chat.send_message(audio_request)
            reply = response.text
            audio = audiobot.get_audio_bytes_from_text(reply.replace("*", ""))
            return SpeechResponse(bytes=audio, message=reply)
        except (AttributeError, ValidationError):
            reply = "Failed to send message to chatbot!"
            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply)
        except gTTSError as e:
            return SpeechResponse(bytes="", message=str(e))
