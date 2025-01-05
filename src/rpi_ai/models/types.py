from __future__ import annotations

from pydantic.dataclasses import dataclass


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
