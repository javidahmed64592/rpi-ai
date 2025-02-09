from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.main import AIApp
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.types import AIConfigType


# Config fixtures
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
    with patch("rpi_ai.types.AIConfigType.load") as mock:
        mock.return_value = mock_config
        yield mock


# Chatbot fixtures
@pytest.fixture
def mock_genai_client() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.chatbot.Client") as mock:
        yield mock


@pytest.fixture
def mock_start_chat_method(mock_genai_client: MagicMock) -> MagicMock:
    mock_chat_instance = MagicMock()
    mock_genai_client.return_value.chats.create.return_value = mock_chat_instance
    mock_chat_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="What's on your mind today?")])
    return mock_genai_client.return_value.chats.create


@pytest.fixture
def mock_chat_instance(mock_start_chat_method: MagicMock) -> MagicMock:
    mock_chat_instance = MagicMock()
    mock_chat_instance.history = [MagicMock(role="model", parts=[MagicMock(text="What's on your mind today?")])]
    mock_start_chat_method.return_value = mock_chat_instance
    return mock_chat_instance


@pytest.fixture
def mock_chatbot(
    mock_app_path: MagicMock,
    mock_api_key: MagicMock,
    mock_config: AIConfigType,
    mock_genai_client: MagicMock,
    mock_chat_instance: MagicMock,
) -> Chatbot:
    return Chatbot(mock_api_key.return_value, mock_config, [])


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
def mock_ai_app_class() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp") as mock:
        yield mock


@pytest.fixture
def mock_app_path() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.root_dir", new_callable=PropertyMock) as mock:
        mock.return_value = Path("/test/app/path")
        yield mock


@pytest.fixture
def mock_api_key() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.api_key", new_callable=PropertyMock) as mock:
        mock.return_value = "test_api_key"
        yield mock


@pytest.fixture
def mock_request_headers() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_headers") as mock:
        yield mock


@pytest.fixture
def mock_request_json() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_json") as mock:
        yield mock


@pytest.fixture
def mock_request_files() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_files") as mock:
        yield mock


@pytest.fixture
def mock_create_new_token() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.create_new_token") as mock:
        mock.return_value = "api_token"
        yield mock


@pytest.fixture
def mock_write_token_to_file() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.write_token_to_file") as mock:
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
