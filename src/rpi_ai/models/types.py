from __future__ import annotations

from pydantic.dataclasses import dataclass


@dataclass
class Message:
    message: str
    is_user_message: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Message:
        parts = "".join([part.text for part in data["parts"]])
        print(parts)
        return cls(parts, data["role"] == "user")


@dataclass
class MessageList:
    messages: list[Message]

    @classmethod
    def from_history(cls, data: list[dict[str, str]]) -> MessageList:
        return cls([Message.from_dict(item) for item in data])
