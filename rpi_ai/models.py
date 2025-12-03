"""API types for the RPi AI application."""

from __future__ import annotations

from datetime import datetime

from google.genai.types import Content, Part
from pydantic import BaseModel, Field
from python_template_server.models import BaseResponse, TemplateServerConfig


# Chatbot Data Models
class ChatbotMessage(BaseModel):
    """ChatbotMessage data type for chat communications."""

    message: str
    timestamp: int
    is_user_message: bool = False

    @classmethod
    def user_message(cls, message: str, timestamp: int) -> ChatbotMessage:
        """Create a user message.

        :param str message:
            ChatbotMessage content
        :param int timestamp:
            ChatbotMessage timestamp
        :return ChatbotMessage:
            User message instance
        """
        return cls(
            message=message,
            timestamp=timestamp,
            is_user_message=True,
        )

    @classmethod
    def model_message(cls, message: str, timestamp: int) -> ChatbotMessage:
        """Create a model message.

        :param str message:
            ChatbotMessage content
        :param int timestamp:
            ChatbotMessage timestamp
        :return ChatbotMessage:
            Model message instance
        """
        return cls(
            message=message,
            timestamp=timestamp,
            is_user_message=False,
        )

    @classmethod
    def new_chat_message(cls, timestamp: int) -> ChatbotMessage:
        """Create a new chat message.

        :param int timestamp:
            ChatbotMessage timestamp
        :return ChatbotMessage:
            New chat message instance
        """
        return cls(
            message="What's on your mind today?",
            timestamp=timestamp,
        )


class ChatbotMessageList(BaseModel):
    """List of messages for chat communications."""

    messages: list[ChatbotMessage]

    @classmethod
    def from_contents_list(cls, contents: list[Content]) -> ChatbotMessageList:
        """Create ChatbotMessageList from Content list.

        :param list[Content] contents:
            List of Content objects
        :return ChatbotMessageList:
            ChatbotMessageList instance
        """
        msgs = []
        for content in contents:
            try:
                if not content.parts or not content.parts[0].text:
                    continue
                match content.role:
                    case "user":
                        msg = ChatbotMessage.user_message(
                            content.parts[0].text.strip(), int(datetime.now().timestamp())
                        )
                    case "model":
                        msg = ChatbotMessage.model_message(
                            content.parts[0].text.strip(), int(datetime.now().timestamp())
                        )
                    case _:
                        continue

                msgs.append(msg)
            except (AttributeError, IndexError):
                pass

        return cls(messages=msgs)

    @property
    def as_contents_list(self) -> list[Content]:
        """Convert ChatbotMessageList to Content list."""
        return [
            Content(
                parts=[Part(text=message.message)],
                role="user" if message.is_user_message else "model",
            )
            for message in self.messages
        ]


class ChatbotSpeech(BaseModel):
    """Speech response data type for audio communications."""

    bytes: str
    message: str
    timestamp: int


# Chatbot Server Configuration Models
class ChatbotConfig(BaseModel):
    """Chatbot configuration model."""

    model: str = Field(default="gemini-2.0-flash", description="LLM to use for chatbot")
    system_instruction: str = Field(
        default="You are a friendly AI assistant. You are designed to help the user with daily tasks.",
        description="System instruction for the chatbot",
    )
    max_output_tokens: int = Field(default=1000, description="Maximum number of output tokens")
    temperature: float = Field(default=1.0, description="Sampling temperature for response generation")


class ChatbotServerConfig(TemplateServerConfig):
    """Chatbot server configuration model."""

    chatbot_config: ChatbotConfig = Field(default_factory=ChatbotConfig, description="Configuration for the AI chatbot")


# Chatbot Server Response Models
class GetConfigResponse(BaseResponse):
    """Get configuration response model."""

    config: ChatbotConfig


class GetChatHistoryResponse(BaseResponse):
    """Get chat history response model."""

    chat_history: ChatbotMessageList


class PostMessageResponse(BaseResponse):
    """Post message response model."""

    reply: ChatbotMessage


class PostAudioResponse(BaseResponse):
    """Post audio response model."""

    reply: ChatbotSpeech
