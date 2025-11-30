"""Pytest fixtures for the RPi AI unit tests."""

import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from prometheus_client import REGISTRY

from rpi_ai.chatbot import Chatbot
from rpi_ai.models import ChatbotConfig, ChatbotServerConfig


# General fixtures
@pytest.fixture(autouse=True)
def mock_here(tmp_path: str) -> Generator[MagicMock, None, None]:
    """Mock the here() function to return a temporary directory."""
    with patch("pyhere.here") as mock_here:
        mock_here.return_value = tmp_path
        yield mock_here


@pytest.fixture(autouse=True)
def mock_env_vars() -> Generator[None, None, None]:
    """Mock environment variables for testing."""
    env_vars = {
        "GEMINI_API_KEY": "test_api_key",
    }
    with patch.dict(os.environ, env_vars) as mock:
        yield mock


@pytest.fixture(autouse=True)
def clear_prometheus_registry() -> Generator[None, None, None]:
    """Clear Prometheus registry before each test to avoid duplicate metric errors."""
    # Clear all collectors from the registry
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    yield
    # Clear again after the test
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)


# Template Server Configuration Models
@pytest.fixture
def mock_chatbot_config_dict() -> dict[str, str | float]:
    """Fixture to provide a sample configuration dictionary."""
    return {
        "model": "test-model",
        "system_instruction": "test-instruction",
        "max_output_tokens": 50,
        "temperature": 0.7,
    }


@pytest.fixture
def mock_chatbot_config(mock_chatbot_config_dict: dict[str, str | float]) -> ChatbotConfig:
    """Fixture to create a mock ChatbotConfig instance."""
    return ChatbotConfig.model_validate(mock_chatbot_config_dict)


@pytest.fixture
def mock_chatbot_server_config(
    mock_chatbot_config: ChatbotConfig,
) -> ChatbotServerConfig:
    """Fixture to create a mock ChatbotServerConfig instance."""
    return ChatbotServerConfig(chatbot_config=mock_chatbot_config)


# Chatbot fixtures
@pytest.fixture
def mock_genai_client() -> Generator[MagicMock, None, None]:
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
    mock_env_vars: MagicMock, mock_chatbot_config: ChatbotConfig, mock_chat_instance: MagicMock
) -> Chatbot:
    """Fixture to create a mock Chatbot instance."""
    return Chatbot(mock_env_vars["GEMINI_API_KEY"], mock_chatbot_config, [])


# Audiobot fixtures
@pytest.fixture
def mock_gtts() -> Generator[MagicMock, None, None]:
    """Mock the gTTS class from the rpi_ai.audiobot module."""
    with patch("rpi_ai.audiobot.gTTS") as mock:
        yield mock


@pytest.fixture
def mock_get_audio_bytes_from_text() -> Generator[MagicMock, None, None]:
    """Mock the get_audio_bytes_from_text function in the rpi_ai.audiobot module."""
    with patch("rpi_ai.audiobot.get_audio_bytes_from_text") as mock:
        yield mock
