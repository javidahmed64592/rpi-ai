from collections.abc import Iterable

from google.genai import Client
from google.genai.types import (
    FunctionResponse,
    GenerateContentConfig,
    GenerateContentResponse,
    GoogleSearchRetrieval,
    Part,
    Tool,
)
from gtts import gTTSError
from pydantic import ValidationError

from rpi_ai.models import audiobot
from rpi_ai.types import AIConfigType, FunctionTool, FunctionToolList, Message, SpeechResponse


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType, functions: FunctionToolList) -> None:
        self._client = Client(api_key=api_key)
        self._config = config
        functions.functions.append(self._web_search)
        self._functions = functions

    def _extract_command_from_part(self, part: Part) -> FunctionTool:
        try:
            return FunctionTool(fn=part.function_call, callable_fn=self._functions[part.function_call.name])
        except (AttributeError, KeyError):
            return None

    def _get_commands_from_response(self, response: GenerateContentResponse) -> Iterable[FunctionTool]:
        commands: Iterable[FunctionResponse] = []
        for part in response.candidates[0].content.parts:
            if command := self._extract_command_from_part(part):
                commands.append(command)
        return commands

    def _get_response_parts_from_commands(self, commands: Iterable[FunctionTool]) -> list[Part]:
        try:
            return [
                Part(function_response=FunctionResponse(name=fn.name, response={"result": fn.response}))
                for fn in commands
            ]
        except AttributeError:
            return []

    def _handle_commands(self, response: GenerateContentResponse) -> GenerateContentResponse:
        if not (commands := self._get_commands_from_response(response)):
            return response

        if not (response_parts := self._get_response_parts_from_commands(commands)):
            return response

        return self._chat.send_message(response_parts)

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
                tools=self._functions.functions,
            ),
        )
        return Message(message="What's on your mind today?")

    def send_message(self, text: str) -> Message:
        response = self._chat.send_message(text)
        response = self._handle_commands(response)

        try:
            return Message(message=response.text)
        except (AttributeError, ValidationError):
            return Message(message="An error occurred! Please try again.")

    def send_audio(self, audio_data: bytes) -> SpeechResponse:
        audio_request = audiobot.get_audio_request(audio_data)
        response = self._chat.send_message(audio_request)

        response = self._handle_commands(response)

        try:
            reply = response.text
            audio = audiobot.get_audio_bytes_from_text(reply.replace("*", ""))
            return SpeechResponse(bytes=audio, message=reply)
        except (AttributeError, ValidationError):
            reply = "Failed to send message to chatbot!"
            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply)
        except gTTSError as e:
            return SpeechResponse(bytes="", message=str(e))
