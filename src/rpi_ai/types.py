from __future__ import annotations

import json

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


# Chatbot responses
@dataclass
class Message:
    message: str
    is_user_message: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Message:
        return cls(message=data["parts"], is_user_message=cls.is_user(data))

    @staticmethod
    def is_user(data: dict[str, str]) -> bool:
        return data["role"] == "user"


@dataclass
class SpeechResponse:
    bytes: str
    message: str
