from collections.abc import Iterable

import google.generativeai as genai
from google.generativeai.protos import FunctionResponse, Part
from google.generativeai.types.generation_types import GenerateContentResponse
from pydantic import ValidationError

from rpi_ai.models.types import AIConfigType, CallableFunctionResponse, FunctionsList, Message


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType, functions: FunctionsList) -> None:
        genai.configure(api_key=api_key)
        self._config = config
        self._functions = functions
        self.initialise_model()

    @property
    def first_message(self) -> dict[str, str]:
        return {"role": "model", "parts": "What's on your mind today?"}

    def _extract_command_from_part(self, part: Part) -> CallableFunctionResponse:
        try:
            return CallableFunctionResponse(fn=part.function_call, callable_fn=self._functions[part.function_call.name])
        except (AttributeError, KeyError):
            return None

    def _get_commands_from_response(self, response: GenerateContentResponse) -> Iterable[CallableFunctionResponse]:
        commands: Iterable[FunctionResponse] = []
        for part in response.parts:
            if command := self._extract_command_from_part(part):
                commands.append(command)
        return commands

    def _get_response_parts_from_commands(self, commands: Iterable[CallableFunctionResponse]) -> list[Part]:
        try:
            return [
                Part(function_response=FunctionResponse(name=fn.name, response={"result": fn.response}))
                for fn in commands
            ]
        except AttributeError:
            return []

    def initialise_model(self) -> None:
        self._model = genai.GenerativeModel(
            model_name=self._config.model,
            system_instruction=self._config.system_instruction,
            generation_config=self._config.generation_config,
            tools=self._functions.functions,
        )

    def get_config(self) -> AIConfigType:
        return self._config

    def update_config(self, config: AIConfigType) -> None:
        self._config = config
        self.initialise_model()

    def start_chat(self) -> Message:
        self._chat = self._model.start_chat(history=[self.first_message])
        return Message(message=self.first_message.get("parts"))

    def send_message(self, text: str) -> Message:
        response = self._chat.send_message(text)

        if commands := self._get_commands_from_response(response):
            if response_parts := self._get_response_parts_from_commands(commands):
                response = self._chat.send_message(response_parts)
        try:
            return Message(message=response.parts[0].text)
        except (AttributeError, ValidationError):
            self._chat.rewind()
            return Message(message="An error occurred! Please try again.")
