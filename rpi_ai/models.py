"""API types for the RPi AI application."""

from __future__ import annotations

from datetime import datetime

from google.genai.types import Content, Part
from pydantic import BaseModel
from python_template_server.models import TemplateServerConfig


# Configuration Models
class ChatbotConfig(BaseModel):
    """Chatbot configuration model."""

    model: str
    system_instruction: str
    max_output_tokens: int
    temperature: float


class ChatbotServerConfig(TemplateServerConfig):
    """Chatbot server configuration model."""

    chatbot_config: ChatbotConfig


# AI Data Models
class Message(BaseModel):
    """Message data type for chat communications."""

    message: str
    timestamp: int
    is_user_message: bool = False

    @classmethod
    def user_message(cls, message: str, timestamp: int) -> Message:
        """Create a user message.

        :param str message:
            Message content
        :param int timestamp:
            Message timestamp
        :return Message:
            User message instance
        """
        return cls(
            message=message,
            timestamp=timestamp,
            is_user_message=True,
        )

    @classmethod
    def model_message(cls, message: str, timestamp: int) -> Message:
        """Create a model message.

        :param str message:
            Message content
        :param int timestamp:
            Message timestamp
        :return Message:
            Model message instance
        """
        return cls(
            message=message,
            timestamp=timestamp,
            is_user_message=False,
        )

    @classmethod
    def new_chat_message(cls, timestamp: int) -> Message:
        """Create a new chat message.

        :param int timestamp:
            Message timestamp
        :return Message:
            New chat message instance
        """
        return cls(
            message="What's on your mind today?",
            timestamp=timestamp,
        )


class MessageList(BaseModel):
    """List of messages for chat communications."""

    messages: list[Message]

    @classmethod
    def from_contents_list(cls, contents: list[Content]) -> MessageList:
        """Create MessageList from Content list.

        :param list[Content] contents:
            List of Content objects
        :return MessageList:
            MessageList instance
        """
        msgs = []
        for content in contents:
            try:
                if not content.parts or not content.parts[0].text:
                    continue
                match content.role:
                    case "user":
                        msg = Message.user_message(content.parts[0].text.strip(), int(datetime.now().timestamp()))
                    case "model":
                        msg = Message.model_message(content.parts[0].text.strip(), int(datetime.now().timestamp()))
                    case _:
                        continue

                msgs.append(msg)
            except (AttributeError, IndexError):
                pass

        return cls(messages=msgs)

    @property
    def as_contents_list(self) -> list[Content]:
        """Convert MessageList to Content list.

        :return list[Content]:
            List of Content objects
        """
        return [
            Content(
                parts=[Part(text=message.message)],
                role="user" if message.is_user_message else "model",
            )
            for message in self.messages
        ]


class SpeechResponse(BaseModel):
    """Speech response data type for audio communications."""

    bytes: str
    message: str
    timestamp: int
