from collections.abc import Iterable

import google.generativeai as genai
from google.generativeai.protos import FunctionResponse, GoogleSearchRetrieval, Part
from google.generativeai.types.content_types import Tool
from google.generativeai.types.generation_types import GenerateContentResponse
from gtts import gTTSError
from pydantic import ValidationError

from rpi_ai.models import audiobot
from rpi_ai.types import AIConfigType, FunctionTool, FunctionToolList, Message, SpeechResponse


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType, functions: FunctionToolList) -> None:
        genai.configure(api_key=api_key)
        self._config = config
        self._functions = functions
        self._web_search_tool = Tool(google_search_retrieval=GoogleSearchRetrieval())
        self._initialise_model()

    def _initialise_model(self) -> None:
        self._model = genai.GenerativeModel(
            model_name=self._config.model,
            system_instruction=self._config.system_instruction,
            generation_config=self._config.generation_config,
            tools=[*self._functions.functions, self._web_search_tool],
        )

    @property
    def first_message(self) -> dict[str, str]:
        return {"role": "model", "parts": "What's on your mind today?"}

    def _extract_command_from_part(self, part: Part) -> FunctionTool:
        try:
            return FunctionTool(fn=part.function_call, callable_fn=self._functions[part.function_call.name])
        except (AttributeError, KeyError):
            return None

    def _get_commands_from_response(self, response: GenerateContentResponse) -> Iterable[FunctionTool]:
        commands: Iterable[FunctionResponse] = []
        for part in response.parts:
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

    def get_config(self) -> AIConfigType:
        return self._config

    def update_config(self, config: AIConfigType) -> None:
        self._config = config
        self._initialise_model()

    def start_chat(self) -> Message:
        self._chat = self._model.start_chat(history=[self.first_message])
        return Message(message=self.first_message.get("parts"))

    def send_message(self, text: str) -> Message:
        response = self._chat.send_message([text])
        has_called_function = False

        if response := self._handle_commands(response):
            has_called_function = True

        try:
            return Message(message=response.parts[0].text)
        except (AttributeError, ValidationError):
            self._chat.rewind()
            if has_called_function:
                self._chat.rewind()
            return Message(message="An error occurred! Please try again.")

    def send_audio(self, audio_data: bytes) -> SpeechResponse:
        request_body = audiobot.get_request_body_from_audio(audio_data)

        response = self._chat.send_message(request_body)
        has_called_function = False

        if response := self._handle_commands(response):
            has_called_function = True

        try:
            reply = response.parts[0].text
            audio = audiobot.get_audio_bytes_from_text(reply.replace("*", ""))
            return SpeechResponse(bytes=audio, message=reply)
        except (AttributeError, ValidationError):
            self._chat.rewind()
            if has_called_function:
                self._chat.rewind()
            reply = "Failed to send message to chatbot!"
            audio = audiobot.get_audio_bytes_from_text(reply)
            return SpeechResponse(bytes=audio, message=reply)
        except gTTSError as e:
            self._chat.rewind()
            if has_called_function:
                self._chat.rewind()
            return SpeechResponse(bytes="", message=str(e))
