from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from rpi_ai.config import AIConfigType
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.types import MessageList


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


class TestChatbot:
    def test_init(
        self,
        mock_chatbot: Chatbot,
        mock_config: AIConfigType,
        mock_api_key: MagicMock,
        mock_genai_configure: MagicMock,
        mock_generative_model: MagicMock,
        mock_start_chat_method: MagicMock,
    ) -> None:
        mock_genai_configure.assert_called_once_with(api_key=mock_api_key.return_value)
        mock_generative_model.assert_called_once_with(
            mock_config.model, generation_config=mock_config.generation_config
        )
        mock_start_chat_method.assert_called_once_with(history=[mock_chatbot.first_message])

    def test_first_message(self, mock_chatbot: Chatbot) -> None:
        assert mock_chatbot.first_message["role"] == "model"
        assert isinstance(mock_chatbot.first_message["parts"], str)

    def test_chat_history(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_extract_parts: MagicMock
    ) -> None:
        data = mock_chatbot.first_message
        mock_extract_parts.return_value = data["parts"]
        expected_history = MessageList.from_history([data])
        assert mock_chatbot.chat_history == expected_history
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_chat(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        user_message = "Hello, world!"
        mock_chat_instance.send_message.return_value.text = user_message
        response = mock_chatbot.chat(user_message)
        assert response == user_message
        mock_chat_instance.send_message.assert_called_once_with(user_message)
