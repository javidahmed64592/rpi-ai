from __future__ import annotations

from google.genai.types import Content, Part
from pydantic.dataclasses import dataclass


@dataclass
class Message:
    message: str
    is_user_message: bool = False

    @classmethod
    def user_message(cls, message: str) -> Message:
        return cls(message=message, is_user_message=True)

    @classmethod
    def model_message(cls, message: str) -> Message:
        return cls(message=message, is_user_message=False)

    @classmethod
    def new_chat_message(cls) -> Message:
        return cls(message="What's on your mind today?")


@dataclass
class MessageList:
    messages: list[Message]

    @classmethod
    def from_contents_list(cls, contents: list[Content]) -> MessageList:
        msgs = []
        for content in contents:
            try:
                if content.role == "user":
                    msg = Message.user_message(content.parts[0].text.strip())
                else:
                    msg = Message.model_message(content.parts[0].text.strip())

                msgs.append(msg)
            except (AttributeError, IndexError):
                pass

        return cls(msgs)

    @property
    def as_contents_list(self) -> list[Content]:
        return [
            Content(parts=[Part(text=message.message)], role="user" if message.is_user_message else "model")
            for message in self.messages
        ]


@dataclass
class SpeechResponse:
    bytes: str
    message: str
