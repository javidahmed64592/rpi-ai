from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from rpi_ai.config import AIConfigType
from rpi_ai.main import AIApp
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.types import Message, MessageList


@pytest.fixture
def mock_api_key() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_api_key") as mock:
        mock.return_value = "test_api_key"
        yield mock


@pytest.fixture
def config_data() -> dict[str, str | float]:
    return {"model": "test-model", "candidate_count": 2, "max_output_tokens": 50, "temperature": 0.7}


@pytest.fixture
def mock_config() -> AIConfigType:
    return AIConfigType("test_model")


@pytest.fixture
def mock_chat_history() -> MessageList:
    return MessageList([Message("Hello, World!")])


@pytest.fixture
def mock_chatbot(
    mock_api_key: MagicMock,
    mock_config: AIConfigType,
    mock_genai_configure: MagicMock,
    mock_generative_model: MagicMock,
    mock_start_chat_method: MagicMock,
    mock_chat_instance: MagicMock,
) -> Chatbot:
    return Chatbot(mock_api_key.return_value, mock_config)


@pytest.fixture
def mock_ai_app(mock_chatbot: MagicMock, mock_api_key: str) -> AIApp:
    return AIApp()
