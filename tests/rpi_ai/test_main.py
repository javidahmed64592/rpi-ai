from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from rpi_ai.main import AIApp
from rpi_ai.models.types import MessageList


@pytest.fixture
def mock_jsonify() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.jsonify") as mock:
        yield mock


@pytest.fixture
def mock_request() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.AIApp.get_request_json") as mock:
        yield mock


@pytest.fixture
def mock_chatbot(mock_chat_history: MessageList) -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.main.Chatbot") as mock:
        mock.chat_history = mock_chat_history
        yield mock


class TestAIApp:
    def test_is_alive(self, mock_ai_app: AIApp, mock_jsonify: MagicMock) -> None:
        response = mock_ai_app.is_alive()
        mock_jsonify.assert_called_once_with({"status": "alive"})
        assert response == mock_jsonify.return_value

    def test_history(self, mock_ai_app: AIApp, mock_api_key: MagicMock, mock_jsonify: MagicMock) -> None:
        response = mock_ai_app.history()
        mock_jsonify.assert_called_once_with(mock_ai_app.chatbot.chat_history)
        assert response == mock_jsonify.return_value

    def test_chat(
        self,
        mock_ai_app: AIApp,
        mock_api_key: MagicMock,
        mock_jsonify: MagicMock,
        mock_request: MagicMock,
        mock_chatbot: MagicMock,
    ) -> None:
        user_message = "Hello, World!"
        mock_request.return_value = {"message": user_message}

        response = mock_ai_app.chat()
        mock_chatbot.return_value.chat.assert_called_once_with(user_message)
        mock_jsonify.assert_called_once_with(mock_ai_app.chatbot.chat_history)
        assert response == mock_jsonify.return_value
