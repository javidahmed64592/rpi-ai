from unittest.mock import MagicMock

from google.genai.types import GenerateContentConfig, GoogleSearch
from gtts import gTTSError

from rpi_ai.models.chatbot import Chatbot
from rpi_ai.types import AIConfigType


class TestChatbot:
    def test_init(self, mock_chatbot: Chatbot, mock_api_key: MagicMock, mock_genai_client: MagicMock) -> None:
        mock_genai_client.assert_called_once_with(api_key=mock_api_key.return_value)

    def test_web_search_config(self, mock_chatbot: Chatbot, mock_config: AIConfigType) -> None:
        config = mock_chatbot._web_search_config()
        assert config.system_instruction == mock_config.system_instruction
        assert config.candidate_count == mock_config.candidate_count
        assert config.max_output_tokens == mock_config.max_output_tokens
        assert config.temperature == mock_config.temperature
        assert len(config.tools) == 1
        assert config.tools[0].google_search == GoogleSearch()

    def test_web_search(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        query = "test query"
        mock_response = MagicMock(text="search results")
        mock_genai_client.return_value.models.generate_content.return_value = mock_response

        result = mock_chatbot._web_search(query)
        mock_genai_client.return_value.models.generate_content.assert_called_once_with(
            contents=query,
            model=mock_chatbot._config.model,
            config=mock_chatbot._web_search_config(),
        )
        assert result == "search results"

    def test_get_config(self, mock_chatbot: Chatbot, mock_config: AIConfigType) -> None:
        assert mock_chatbot.get_config() == mock_config

    def test_update_config(
        self,
        mock_chatbot: Chatbot,
        mock_config: AIConfigType,
    ) -> None:
        mock_config.model = "new-model"
        mock_chatbot.update_config(mock_config)
        assert mock_chatbot.get_config() == mock_config

    def test_start_chat(self, mock_chatbot: Chatbot, mock_start_chat_method: MagicMock) -> None:
        response = mock_chatbot.start_chat()
        mock_start_chat_method.assert_called_once_with(
            model=mock_chatbot._config.model,
            config=GenerateContentConfig(
                system_instruction=mock_chatbot._config.system_instruction,
                candidate_count=mock_chatbot._config.candidate_count,
                max_output_tokens=mock_chatbot._config.max_output_tokens,
                temperature=mock_chatbot._config.temperature,
                tools=mock_chatbot._functions,
            ),
        )
        assert response.message == "What's on your mind today?"

    def test_send_message_with_valid_response(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "Hi user!"

    def test_send_message_with_error(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_chat_instance.send_message.return_value = MagicMock(text=None)

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "An error occurred! Please try again."

    def test_send_audio_with_valid_response(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        mock_audio = "test_audio_response"
        mock_get_audio_bytes_from_text.return_value = mock_audio
        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Hi user!"
        assert response.bytes == mock_audio

    def test_send_audio_with_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.parts = [MagicMock(text=None)]
        mock_chat_instance.send_message.return_value = mock_response

        mock_audio = "Failed to send messages to chatbot!"
        mock_get_audio_bytes_from_text.return_value = mock_audio

        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Failed to send message to chatbot!"
        assert response.bytes == mock_audio

    def test_send_audio_with_gtts_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_chat_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="Hi user!")])
        mock_get_audio_bytes_from_text.side_effect = gTTSError("gTTS error")

        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "gTTS error"
        assert response.bytes == ""
