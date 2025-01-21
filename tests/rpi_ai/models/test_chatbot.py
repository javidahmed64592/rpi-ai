from unittest.mock import MagicMock

from rpi_ai.config import AIConfigType
from rpi_ai.models.chatbot import Chatbot


class TestChatbot:
    def test_init(
        self,
        mock_chatbot: Chatbot,
        mock_config: AIConfigType,
        mock_api_key: MagicMock,
        mock_genai_configure: MagicMock,
        mock_generative_model: MagicMock,
    ) -> None:
        mock_genai_configure.assert_called_once_with(api_key=mock_api_key.return_value)
        mock_generative_model.assert_called_once_with(
            mock_config.model, generation_config=mock_config.generation_config
        )

    def test_first_message(self, mock_chatbot: Chatbot) -> None:
        assert mock_chatbot.first_message["role"] == "model"
        assert isinstance(mock_chatbot.first_message["parts"], str)

    def test_start_chat(self, mock_chatbot: Chatbot, mock_start_chat_method: MagicMock) -> None:
        response = mock_chatbot.start_chat()
        mock_start_chat_method.assert_called_once_with(history=[mock_chatbot.first_message])
        assert response.message == mock_chatbot.first_message["parts"]

    def test_send_message(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_response = "Hi user!"
        mock_chat_instance.send_message.return_value.text = mock_response

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == mock_response

    def test_send_command(self, mock_chatbot: Chatbot, mock_generate_content: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_response = "Hi user!"
        mock_generate_content.return_value.text = mock_response

        response = mock_chatbot.send_command(mock_msg)
        mock_generate_content.assert_called_once_with(mock_msg)
        assert response.message == mock_response
