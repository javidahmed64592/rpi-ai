"""Pytest fixtures for the RPi AI unit tests."""

import os
from collections.abc import Generator
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.config import ChatbotConfig
from rpi_ai.main import AIApp
from rpi_ai.models.chatbot import Chatbot


# Config fixtures
@pytest.fixture(autouse=True)
def mock_env_vars() -> Generator[None, None, None]:
    """Mock environment variables for testing."""
    env_vars = {
        "RPI_AI_PATH": "/test/app/path",
        "GEMINI_API_KEY": "test_api_key",
    }
    with patch.dict(os.environ, env_vars) as mock:
        yield mock


@pytest.fixture
def mock_generate_token() -> Generator[MagicMock, None, None]:
    """Mock the generate_token method in the Config class."""
    with patch("rpi_ai.config.Config.generate_token") as mock:
        yield mock


@pytest.fixture
def config_data() -> dict[str, str | float]:
    """Fixture to provide a sample configuration dictionary."""
    return {
        "model": "test-model",
        "system_instruction": "test-instruction",
        "max_output_tokens": 50,
        "temperature": 0.7,
    }


@pytest.fixture
def mock_config(config_data: dict[str, str | float]) -> ChatbotConfig:
    """Fixture to create a mock ChatbotConfig instance."""
    return ChatbotConfig(**config_data)


@pytest.fixture
def mock_load_config(mock_config: ChatbotConfig) -> Generator[MagicMock, None, None]:
    """Mock the load method of ChatbotConfig to return a predefined config."""
    with patch("rpi_ai.config.ChatbotConfig.load") as mock:
        mock.return_value = mock_config
        yield mock


@pytest.fixture
def mock_save_config() -> Generator[MagicMock, None, None]:
    """Mock the save method of ChatbotConfig."""
    with patch("rpi_ai.config.ChatbotConfig.save") as mock:
        yield mock


# Chatbot fixtures
@pytest.fixture
def mock_genai_client() -> Generator[MagicMock, None, None]:
    """Mock the Client class from the rpi_ai.models.chatbot module."""
    with patch("rpi_ai.models.chatbot.Client") as mock:
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
def mock_chatbot(mock_env_vars: MagicMock, mock_config: ChatbotConfig, mock_chat_instance: MagicMock) -> Chatbot:
    """Fixture to create a mock Chatbot instance."""
    return Chatbot(mock_env_vars["GEMINI_API_KEY"], mock_config, [])


@pytest.fixture
def mock_chat_history() -> Generator[MagicMock, None, None]:
    """Mock the chat_history property of the Chatbot class."""
    with patch("rpi_ai.main.Chatbot.chat_history", new_callable=PropertyMock) as mock:
        yield mock


@pytest.fixture
def mock_get_config(mock_config: ChatbotConfig) -> Generator[MagicMock, None, None]:
    """Mock the get_config method of the Chatbot class to return a predefined config."""
    with patch("rpi_ai.main.Chatbot.get_config") as mock:
        mock.return_value = mock_config
        yield mock


@pytest.fixture
def mock_update_config() -> Generator[MagicMock, None, None]:
    """Mock the update_config method of the Chatbot class."""
    with patch("rpi_ai.main.Chatbot.update_config") as mock:
        yield mock


@pytest.fixture
def mock_start_chat() -> Generator[MagicMock, None, None]:
    """Mock the start_chat method of the Chatbot class."""
    with patch("rpi_ai.main.Chatbot.start_chat") as mock:
        yield mock


@pytest.fixture
def mock_send_message() -> Generator[MagicMock, None, None]:
    """Mock the send_message method of the Chatbot class."""
    with patch("rpi_ai.main.Chatbot.send_message") as mock:
        yield mock


@pytest.fixture
def mock_send_audio() -> Generator[MagicMock, None, None]:
    """Mock the send_audio method of the Chatbot class."""
    with patch("rpi_ai.main.Chatbot.send_audio") as mock:
        yield mock


# Audiobot fixtures
@pytest.fixture
def mock_gtts() -> Generator[MagicMock, None, None]:
    """Mock the gTTS class from the rpi_ai.models.audiobot module."""
    with patch("rpi_ai.models.audiobot.gTTS") as mock:
        yield mock


@pytest.fixture
def mock_get_audio_bytes_from_text() -> Generator[MagicMock, None, None]:
    """Mock the get_audio_bytes_from_text function in the rpi_ai.models.audiobot module."""
    with patch("rpi_ai.models.audiobot.get_audio_bytes_from_text") as mock:
        yield mock


# AIApp fixtures
@pytest.fixture
def mock_jsonify() -> Generator[MagicMock, None, None]:
    """Mock the jsonify function from Flask."""
    with patch("rpi_ai.main.jsonify") as mock:
        yield mock


@pytest.fixture
def mock_request_headers() -> Generator[MagicMock, None, None]:
    """Mock the get_request_headers function in the rpi_ai.main module."""
    with patch("rpi_ai.main.get_request_headers") as mock:
        yield mock


@pytest.fixture
def mock_request_json() -> Generator[MagicMock, None, None]:
    """Mock the get_request_json function in the rpi_ai.main module."""
    with patch("rpi_ai.main.get_request_json") as mock:
        yield mock


@pytest.fixture
def mock_request_files() -> Generator[MagicMock, None, None]:
    """Mock the get_request_files function in the rpi_ai.main module."""
    with patch("rpi_ai.main.get_request_files") as mock:
        yield mock


@pytest.fixture
def mock_ai_app_class() -> Generator[MagicMock, None, None]:
    """Mock the AIApp class in the rpi_ai.main module."""
    with patch("rpi_ai.main.AIApp") as mock:
        yield mock


@pytest.fixture
def mock_ai_app(mock_chatbot: Chatbot, mock_load_config: MagicMock, mock_generate_token: MagicMock) -> AIApp:
    """Fixture to create a mock AIApp instance."""
    app = AIApp()
    app.chatbot = mock_chatbot
    return app


@pytest.fixture
def mock_client(mock_ai_app: AIApp) -> Generator[FlaskClient, None, None]:
    """Fixture to create a mock Flask client for testing."""
    with mock_ai_app._app.test_client() as client:
        yield client


@pytest.fixture
def mock_waitress_serve() -> Generator[MagicMock, None, None]:
    """Mock the serve function in the rpi_ai.main module."""
    with patch("rpi_ai.main.serve") as mock:
        yield mock
