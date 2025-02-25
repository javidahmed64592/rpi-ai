import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.api_types import AIConfigType
from rpi_ai.main import AIApp
from rpi_ai.models.chatbot import Chatbot


# Config fixtures
@pytest.fixture(autouse=True)
def mock_env_vars() -> Generator[None, None, None]:
    env_vars = {
        "RPI_AI_PATH": "/test/app/path",
        "GEMINI_API_KEY": "test_api_key",
    }
    with patch.dict(os.environ, env_vars) as mock:
        yield mock


@pytest.fixture
def config_data() -> dict[str, str | float]:
    return {
        "model": "test-model",
        "system_instruction": "test-instruction",
        "candidate_count": 2,
        "max_output_tokens": 50,
        "temperature": 0.7,
    }


@pytest.fixture
def mock_config(config_data: dict[str, str | float]) -> AIConfigType:
    return AIConfigType(**config_data)


@pytest.fixture
def mock_load_config(mock_config: AIConfigType) -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.api_types.AIConfigType.load") as mock:
        mock.return_value = mock_config
        yield mock


@pytest.fixture
def mock_save_config() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.api_types.AIConfigType.save") as mock:
        yield mock


# Chatbot fixtures
@pytest.fixture
def mock_genai_client() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.chatbot.Client") as mock:
        yield mock


@pytest.fixture
def mock_chat_instance(mock_genai_client: MagicMock) -> MagicMock:
    mock_instance = MagicMock()
    mock_genai_client.return_value.chats.create.return_value = mock_instance
    mock_instance._curated_history = [MagicMock(parts=[MagicMock(text="What's on your mind today?")], role="model")]
    mock_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="Hi user!")])
    return mock_instance


@pytest.fixture
def mock_chatbot(mock_env_vars: MagicMock, mock_config: AIConfigType, mock_chat_instance: MagicMock) -> Chatbot:
    return Chatbot(mock_env_vars["GEMINI_API_KEY"], mock_config, [])


@pytest.fixture
def mock_get_config(mock_config: AIConfigType) -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.get_config") as mock:
        mock.return_value = mock_config
        yield mock


@pytest.fixture
def mock_update_config() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.update_config") as mock:
        yield mock


@pytest.fixture
def mock_get_chat_history() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.get_chat_history") as mock:
        yield mock


@pytest.fixture
def mock_start_chat() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.start_chat") as mock:
        yield mock


@pytest.fixture
def mock_send_message() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.send_message") as mock:
        yield mock


@pytest.fixture
def mock_send_audio() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.send_audio") as mock:
        yield mock


# Audiobot fixtures
@pytest.fixture
def mock_gtts() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.audiobot.gTTS") as mock:
        yield mock


@pytest.fixture
def mock_get_audio_bytes_from_text() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.audiobot.get_audio_bytes_from_text") as mock:
        yield mock


# AIApp fixtures
@pytest.fixture
def mock_jsonify() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.jsonify") as mock:
        yield mock


@pytest.fixture
def mock_request_headers() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.get_request_headers") as mock:
        yield mock


@pytest.fixture
def mock_request_json() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.get_request_json") as mock:
        yield mock


@pytest.fixture
def mock_request_files() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.get_request_files") as mock:
        yield mock


@pytest.fixture
def mock_ai_app_class() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp") as mock:
        yield mock


@pytest.fixture
def mock_load_token_from_file() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp._load_token_from_file") as mock:
        yield mock


@pytest.fixture
def mock_create_new_token() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp._create_new_token") as mock:
        yield mock


@pytest.fixture
def mock_write_token_to_file() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp._write_token_to_file") as mock:
        yield mock


@pytest.fixture
def mock_ai_app(
    mock_chatbot: Chatbot,
    mock_load_config: MagicMock,
    mock_create_new_token: MagicMock,
    mock_write_token_to_file: MagicMock,
) -> AIApp:
    app = AIApp()
    app.chatbot = mock_chatbot
    return app


@pytest.fixture
def mock_client(mock_ai_app: AIApp) -> Generator[FlaskClient, None, None]:
    with mock_ai_app.app.test_client() as client:
        yield client


@pytest.fixture
def mock_waitress_serve() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.serve") as mock:
        yield mock
