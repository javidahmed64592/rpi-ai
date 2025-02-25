from __future__ import annotations

import json

from google.genai.types import Content, Part
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

    def save(self, path: str) -> None:
        with open(path, "w") as file:
            json.dump(self.__dict__, file, indent=4)


# Chatbot responses
@dataclass
class Message:
    message: str
    is_user_message: bool = False


@dataclass
class MessageList:
    messages: list[Message]

    @classmethod
    def from_contents_list(cls, contents: list[Content]) -> MessageList:
        message_list = cls([])
        for content in contents:
            try:
                if content.role == "user":
                    message_list.add_user_message(content.parts[0].text.strip())
                else:
                    message_list.add_model_message(content.parts[0].text.strip())
            except (AttributeError, IndexError):
                pass
        return message_list

    @property
    def history(self) -> list[Content]:
        return [
            Content(parts=[Part(text=message.message)], role="user" if message.is_user_message else "model")
            for message in self.messages
        ]

    def add_user_message(self, message: str) -> None:
        self.messages.append(Message(message=message, is_user_message=True))

    def add_model_message(self, message: str) -> None:
        self.messages.append(Message(message=message, is_user_message=False))


@dataclass
class SpeechResponse:
    bytes: str
    message: str
