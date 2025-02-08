from __future__ import annotations

import json
from collections.abc import Callable

from google.generativeai.protos import FunctionCall
from google.generativeai.types import GenerationConfig
from pydantic.dataclasses import dataclass


# Config
@dataclass
class AIConfigType:
    model: str
    system_instruction: str
    candidate_count: int = 1
    max_output_tokens: int = 20
    temperature: float = 1.0

    @classmethod
    def load(cls, path: str) -> AIConfigType:
        with open(path) as file:
            return cls(**json.load(file))

    @property
    def generation_config(self) -> GenerationConfig:
        return GenerationConfig(
            candidate_count=self.candidate_count,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )


# Chatbot responses
@dataclass
class Message:
    message: str
    is_user_message: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Message:
        parts = Message.extract_parts(data).strip()
        is_user = Message.is_user(data)
        return cls(parts, is_user)

    @staticmethod
    def extract_parts(data: dict[str, str]) -> str:
        return "".join([part.text for part in data["parts"]])

    @staticmethod
    def is_user(data: dict[str, str]) -> bool:
        return data["role"] == "user"


@dataclass
class MessageList:
    messages: list[Message]

    @classmethod
    def from_history(cls, data: list[dict[str, str]]) -> MessageList:
        return cls([Message.from_dict(item) for item in data])


@dataclass
class SpeechResponse:
    bytes: str
    message: str


# Functions
class FunctionTool:
    def __init__(self, fn: FunctionCall, callable_fn: Callable) -> None:
        self.function = fn
        self.callable_fn = callable_fn

    @property
    def name(self) -> str:
        return self.function.name

    @property
    def args(self) -> dict[str, str]:
        return ", ".join(f"{key}={val}" for key, val in self.function.args.items())

    @property
    def response(self) -> dict[str, str]:
        if self.function.args:
            return self.callable_fn(**self.function.args)
        return self.callable_fn()

    @property
    def output(self) -> str:
        return f"{self.name}({self.args})={self.response}"


@dataclass
class FunctionToolList:
    functions: list[Callable]

    @property
    def dictionary(self) -> dict[str, str]:
        return {fn.__name__: fn for fn in self.functions}

    def __getitem__(self, name: str) -> Callable:
        return self.dictionary[name]
