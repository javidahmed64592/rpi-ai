from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.config import AIConfigType
from rpi_ai.main import AIApp
from rpi_ai.models.chatbot import Chatbot


# Config fixtures
@pytest.fixture
def config_data() -> dict[str, str | float]:
    return {"model": "test-model", "candidate_count": 2, "max_output_tokens": 50, "temperature": 0.7}


@pytest.fixture
def mock_config(config_data: dict[str, str | float]) -> AIConfigType:
    return AIConfigType(**config_data)


# Chatbot fixtures
@pytest.fixture
def mock_api_key() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_api_key") as mock:
        mock.return_value = "test_api_key"
        yield mock


@pytest.fixture
def mock_genai_configure() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.chatbot.genai.configure") as mock:
        yield mock


@pytest.fixture
def mock_generative_model() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.chatbot.genai.GenerativeModel") as mock:
        yield mock


@pytest.fixture
def mock_start_chat_method(mock_generative_model: MagicMock) -> MagicMock:
    mock_chat_instance = MagicMock()
    mock_generative_model.return_value.start_chat.return_value = mock_chat_instance
    return mock_generative_model.return_value.start_chat


@pytest.fixture
def mock_chat_instance(mock_start_chat_method: MagicMock) -> MagicMock:
    mock_chat_instance = MagicMock()
    mock_chat_instance.history = [MagicMock(role="model", parts="What's on your mind today")]
    mock_start_chat_method.return_value = mock_chat_instance
    return mock_chat_instance


@pytest.fixture
def mock_chatbot(
    mock_api_key: MagicMock,
    mock_config: AIConfigType,
    mock_genai_configure: MagicMock,
    mock_chat_instance: MagicMock,
) -> Chatbot:
    return Chatbot(mock_api_key.return_value, mock_config)


@pytest.fixture
def mock_start_chat() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.start_chat") as mock:
        yield mock


@pytest.fixture
def mock_send_message() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot.send_message") as mock:
        yield mock


# AIApp fixtures
@pytest.fixture
def mock_jsonify() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.jsonify") as mock:
        yield mock


@pytest.fixture
def mock_request_json() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_json") as mock:
        yield mock


@pytest.fixture
def mock_request_headers() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_headers") as mock:
        yield mock


@pytest.fixture
def mock_ai_app(mock_chatbot: Chatbot) -> AIApp:
    app = AIApp()
    app.token = "test_token"
    app.chatbot = mock_chatbot
    return app


@pytest.fixture
def mock_client(mock_ai_app: AIApp) -> Generator[FlaskClient, None, None]:
    with mock_ai_app.app.test_client() as client:
        yield client
