"""Pytest fixtures for the RPi AI unit tests."""

import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from rpi_ai.chatbot import Chatbot
from rpi_ai.models import (
    ChatbotConfig,
    ChatbotMessage,
    ChatbotMessageList,
    ChatbotServerConfig,
    ChatbotSpeech,
    ChatMemoryEntry,
    ChatMemoryList,
    EmbeddingConfig,
)


# General fixtures
@pytest.fixture
def mock_json_dump() -> Generator[MagicMock]:
    """Mock the json.dump() method."""
    with patch("json.dump") as mock_dump:
        yield mock_dump


@pytest.fixture
def mock_json_load() -> Generator[MagicMock]:
    """Mock the json.load() method."""
    with patch("json.load") as mock_load:
        yield mock_load


@pytest.fixture
def mock_exists() -> Generator[MagicMock]:
    """Mock the Path.exists() method."""
    with patch("pathlib.Path.exists") as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_path_home() -> Generator[MagicMock]:
    """Mock the Path.home() method."""
    with patch("pathlib.Path.home") as mock_home:
        yield mock_home


@pytest.fixture(autouse=True)
def mock_open_file() -> Generator[MagicMock]:
    """Mock the Path.open() method."""
    with patch("pathlib.Path.open", mock_open()) as mock_file:
        yield mock_file


@pytest.fixture(autouse=True)
def mock_env_vars() -> Generator[MagicMock]:
    """Mock environment variables for testing."""
    env_vars = {
        "GEMINI_API_KEY": "test_api_key",
    }
    with patch.dict(os.environ, env_vars) as mock:
        yield mock


# Chatbot Data Models
@pytest.fixture
def mock_chatbot_message_user_dict() -> dict:
    """Fixture to provide a sample user ChatbotMessage dictionary."""
    return {
        "message": "user message",
        "timestamp": 123,
        "is_user_message": True,
    }


@pytest.fixture
def mock_chatbot_message_model_dict() -> dict:
    """Fixture to provide a sample model ChatbotMessage dictionary."""
    return {
        "message": "model message",
        "timestamp": 124,
        "is_user_message": False,
    }


@pytest.fixture
def mock_chatbot_message_list_dict(
    mock_chatbot_message_user_dict: dict,
    mock_chatbot_message_model_dict: dict,
) -> dict:
    """Fixture to provide a sample ChatbotMessageList dictionary."""
    return {
        "messages": [
            mock_chatbot_message_user_dict,
            mock_chatbot_message_model_dict,
        ]
    }


@pytest.fixture
def mock_chatbot_speech_dict() -> dict:
    """Fixture to provide a sample ChatbotSpeech dictionary."""
    return {
        "bytes": "audio_data",
        "message": "Hello, world!",
        "timestamp": 125,
    }


@pytest.fixture
def mock_chatbot_message_user(mock_chatbot_message_user_dict: dict) -> ChatbotMessage:
    """Fixture to create a mock user ChatbotMessage instance."""
    return ChatbotMessage.model_validate(mock_chatbot_message_user_dict)


@pytest.fixture
def mock_chatbot_message_model(mock_chatbot_message_model_dict: dict) -> ChatbotMessage:
    """Fixture to create a mock model ChatbotMessage instance."""
    return ChatbotMessage.model_validate(mock_chatbot_message_model_dict)


@pytest.fixture
def mock_chatbot_message_list(mock_chatbot_message_list_dict: dict) -> ChatbotMessageList:
    """Fixture to create a mock ChatbotMessageList instance."""
    return ChatbotMessageList.model_validate(mock_chatbot_message_list_dict)


@pytest.fixture
def mock_chatbot_speech(mock_chatbot_speech_dict: dict) -> ChatbotSpeech:
    """Fixture to create a mock ChatbotSpeech instance."""
    return ChatbotSpeech.model_validate(mock_chatbot_speech_dict)


# Memory Models
@pytest.fixture
def mock_chat_memory_entry_dict() -> dict:
    """Fixture to provide a sample ChatMemoryEntry dictionary."""
    return {
        "text": "Test memory entry",
        "vector": [0.1, 0.2, 0.3],
    }


@pytest.fixture
def mock_chat_memory_entry(mock_chat_memory_entry_dict: dict) -> ChatMemoryEntry:
    """Fixture to create a mock ChatMemoryEntry instance."""
    return ChatMemoryEntry.model_validate(mock_chat_memory_entry_dict)


@pytest.fixture
def mock_chat_memory_list(mock_chat_memory_entry: ChatMemoryEntry) -> ChatMemoryList:
    """Fixture to create a mock ChatMemoryList instance."""
    return ChatMemoryList(entries=[mock_chat_memory_entry])


# Chatbot Server Configuration Models
@pytest.fixture
def mock_chatbot_config_dict() -> dict:
    """Fixture to provide a sample configuration dictionary."""
    return {
        "model": "test-model",
        "system_instruction": "test-instruction",
        "max_output_tokens": 50,
        "temperature": 0.7,
    }


@pytest.fixture
def mock_embedding_config_dict() -> dict:
    """Fixture to provide a sample embedding configuration dictionary."""
    return {
        "model": "gemini-embedding-001",
        "memory_filepath": "chat_memory.json",
        "max_memories": 5,
        "top_k": 3,
    }


@pytest.fixture
def mock_chatbot_config(mock_chatbot_config_dict: dict) -> ChatbotConfig:
    """Fixture to create a mock ChatbotConfig instance."""
    return ChatbotConfig.model_validate(mock_chatbot_config_dict)


@pytest.fixture
def mock_embedding_config(mock_embedding_config_dict: dict) -> EmbeddingConfig:
    """Fixture to create a mock EmbeddingConfig instance."""
    return EmbeddingConfig.model_validate(mock_embedding_config_dict)


@pytest.fixture
def mock_chatbot_server_config(
    mock_chatbot_config: ChatbotConfig,
    mock_embedding_config: EmbeddingConfig,
) -> ChatbotServerConfig:
    """Fixture to create a mock ChatbotServerConfig instance."""
    return ChatbotServerConfig(chatbot_config=mock_chatbot_config, embedding_config=mock_embedding_config)


# Chatbot fixtures
@pytest.fixture
def mock_genai_client() -> Generator[MagicMock]:
    """Mock the Client class from the rpi_ai.chatbot module."""
    with patch("rpi_ai.chatbot.Client") as mock:
        yield mock


@pytest.fixture
def mock_chat_instance(mock_genai_client: MagicMock) -> MagicMock:
    """Mock a chat instance from the genai client."""
    mock_instance = MagicMock()
    mock_genai_client.return_value.chats.create.return_value = mock_instance
    mock_instance._curated_history = [MagicMock(parts=[MagicMock(text="What's on your mind today?")], role="model")]
    mock_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="Hi user!")])
    return mock_instance


@pytest.fixture
def mock_chatbot(
    mock_env_vars: MagicMock,
    mock_chatbot_config: ChatbotConfig,
    mock_embedding_config: EmbeddingConfig,
    mock_chat_memory_list: ChatMemoryList,
    mock_chat_instance: MagicMock,
) -> Chatbot:
    """Fixture to create a mock Chatbot instance."""
    return Chatbot(
        api_key=mock_env_vars["GEMINI_API_KEY"],
        config_dir=Path("/mock/config/dir"),
        config=mock_chatbot_config,
        embedding_config=mock_embedding_config,
        functions=[],
        memories=mock_chat_memory_list,
    )


# Audiobot fixtures
@pytest.fixture
def mock_gtts() -> Generator[MagicMock]:
    """Mock the gTTS class from the rpi_ai.audiobot module."""
    with patch("rpi_ai.audiobot.gTTS") as mock:
        yield mock


@pytest.fixture
def mock_get_audio_bytes_from_text() -> Generator[MagicMock]:
    """Mock the get_audio_bytes_from_text function in the rpi_ai.audiobot module."""
    with patch("rpi_ai.audiobot.get_audio_bytes_from_text") as mock:
        yield mock
