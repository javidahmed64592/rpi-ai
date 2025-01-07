from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.main import AIApp
from rpi_ai.models.types import MessageList


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
def mock_chatbot(mock_chat_history: MessageList) -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot") as mock:
        mock.chat_history = mock_chat_history
        yield mock


class TestAIApp:
    def test_is_alive(self, mock_client: FlaskClient, mock_jsonify: MagicMock) -> None:
        response = mock_client.get("/")
        mock_jsonify.assert_called_once_with({"status": "alive"})
        assert response.status_code == 200

    def test_authenticate_success(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        assert mock_ai_app.authenticate() is True

    def test_authenticate_failure(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        assert mock_ai_app.authenticate() is False

    def test_history(
        self, mock_ai_app: AIApp, mock_client: FlaskClient, mock_request_headers: MagicMock, mock_jsonify: MagicMock
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        response = mock_client.get("/history")
        mock_jsonify.assert_called_once_with(mock_ai_app.chatbot.chat_history)
        assert response.status_code == 200

    def test_history_unauthorized(
        self, mock_client: FlaskClient, mock_request_headers: MagicMock, mock_jsonify: MagicMock
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        response = mock_client.get("/history")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == 401

    def test_chat(
        self,
        mock_ai_app: AIApp,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
        mock_chatbot: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/chat")
        mock_chatbot.return_value.chat.assert_called_once_with(user_message)
        mock_jsonify.assert_called_once_with(mock_ai_app.chatbot.chat_history)
        assert response.status_code == 200

    def test_chat_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/chat")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == 401
