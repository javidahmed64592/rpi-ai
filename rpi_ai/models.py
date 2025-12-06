"""API types for the RPi AI application."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
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


# Memory Models
class ChatMemoryEntry(BaseModel):
    """Chat memory entry data type."""

    text: str
    vector: list[float]


class ChatMemoryList(BaseModel):
    """List of chat memory entries."""

    entries: list[ChatMemoryEntry]

    def add_entry(self, text: str, vector: list[float]) -> None:
        """Add a chat memory entry to the list.

        :param ChatMemoryEntry entry:
            Chat memory entry to add
        """
        self.entries.append(ChatMemoryEntry(text=text, vector=vector))

    def clear_entries(self) -> None:
        """Clear all chat memory entries."""
        self.entries.clear()

    def retrieve_memories(self, query_vector: list[float], top_k: int) -> list[str]:
        """Retrieve top-k similar chat memory entries based on cosine similarity.

        :param list[float] query_vector:
            Query vector for similarity comparison
        :param int top_k:
            Number of top similar entries to retrieve
        :return list[str]:
            List of text from top-k similar chat memory entries
        """
        sims = [
            np.dot(query_vector, m.vector) / (np.linalg.norm(query_vector) * np.linalg.norm(m.vector))
            for m in self.entries
        ]
        return [self.entries[i].text for i in np.argsort(sims)[-top_k:][::-1]]

    def save_to_file(self, filepath: Path) -> None:
        """Save chat memory entries to a JSON file.

        :param Path filepath:
            Filepath to save the chat memory entries
        """
        with filepath.open("w") as f:
            json.dump(self.model_dump(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: Path) -> ChatMemoryList:
        """Load chat memory entries from a JSON file.

        :param Path filepath:
            Filepath to load the chat memory entries from
        """
        try:
            with filepath.open() as f:
                data = json.load(f)
            return cls.model_validate(data)
        except FileNotFoundError:
            return cls(entries=[])


# Chatbot Server Configuration Models
class ChatbotConfig(BaseModel):
    """Chatbot configuration model."""

    model: str = Field(default="gemini-2.0-flash", description="LLM to use for chatbot")
    system_instruction: str = Field(
        default=(
            "You are a friendly AI assistant designed to help the user with daily tasks. "
            "You have a persistent memory system that allows you to remember facts about the user across conversations."
        ),
        description="System instruction for the chatbot",
    )
    max_output_tokens: int = Field(default=1000, description="Maximum number of output tokens")
    temperature: float = Field(default=1.0, description="Sampling temperature for response generation")

    @staticmethod
    def get_memory_guidelines() -> str:
        """Get memory guidelines for the chatbot system instruction."""
        return (
            "MEMORY GUIDELINES:\n"
            "- When the user shares personal information (preferences, likes, dislikes, facts about "
            "their life, goals, etc.), call the `create_memory` function to store it for future reference.\n"
            "- At the start of each conversation or when context about the user would be helpful, "
            "call the `retrieve_memories` function with relevant keywords from the user's message "
            "to recall what you know.\n"
            "- Use retrieved memories naturally in your responses to provide personalized, context-aware assistance.\n"
            "- Examples of facts to remember: favorite music/movies, dietary preferences, hobbies, work information, "
            "family details, goals, past conversations, scheduled events.\n\n"
            "Be proactive in using your memory to create a personalized experience for the user."
        )


class EmbeddingConfig(BaseModel):
    """Embedding configuration model."""

    model: str = Field(default="gemini-embedding-001", description="Embedding model to use")
    memory_filepath: str = Field(default="chat_memory.json", description="Filepath to store chat memory embeddings")
    top_k: int = Field(default=5, description="Number of top similar memories to retrieve")


class ChatbotServerConfig(TemplateServerConfig):
    """Chatbot server configuration model."""

    chatbot_config: ChatbotConfig = Field(default_factory=ChatbotConfig, description="Configuration for the AI chatbot")
    embedding_config: EmbeddingConfig = Field(
        default_factory=EmbeddingConfig, description="Configuration for the embedding model"
    )


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
