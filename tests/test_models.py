"""Unit tests for the rpi_ai.models module."""

from google.genai.types import Content, Part
from python_template_server.models import ResponseCode

from rpi_ai.models import (
    ChatbotConfig,
    ChatbotMessage,
    ChatbotMessageList,
    ChatbotServerConfig,
    ChatbotSpeech,
    GetChatHistoryResponse,
    GetConfigResponse,
    PostAudioResponse,
    PostMessageResponse,
)


# Chatbot Data Models
class TestChatbotMessage:
    """Tests for the ChatbotMessage class."""

    def test_model_dump(self, mock_chatbot_message_user_dict: dict, mock_chatbot_message_user: ChatbotMessage) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_message_user.model_dump() == mock_chatbot_message_user_dict

    def test_user_message(self, mock_chatbot_message_user_dict: dict) -> None:
        """Test creating a user message."""
        chatbot_message = ChatbotMessage.user_message(
            mock_chatbot_message_user_dict["message"], mock_chatbot_message_user_dict["timestamp"]
        )
        assert chatbot_message.model_dump() == mock_chatbot_message_user_dict

    def test_model_message(self, mock_chatbot_message_model_dict: dict) -> None:
        """Test creating a model message."""
        chatbot_message = ChatbotMessage.model_message(
            mock_chatbot_message_model_dict["message"], mock_chatbot_message_model_dict["timestamp"]
        )
        assert chatbot_message.model_dump() == mock_chatbot_message_model_dict

    def test_new_chat_message(self) -> None:
        """Test creating a new chat message."""
        expected_dict = {
            "message": "What's on your mind today?",
            "timestamp": 1234567890,
            "is_user_message": False,
        }
        assert isinstance(expected_dict["timestamp"], int)
        chatbot_message = ChatbotMessage.new_chat_message(expected_dict["timestamp"])
        assert chatbot_message.model_dump() == expected_dict


class TestChatbotMessageList:
    """Tests for the ChatbotMessageList class."""

    def test_model_dump(
        self, mock_chatbot_message_list_dict: dict, mock_chatbot_message_list: ChatbotMessageList
    ) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_message_list.model_dump() == mock_chatbot_message_list_dict

    def test_history(self, mock_chatbot_message_list_dict: dict) -> None:
        """Test converting a ChatbotMessageList to a history list."""
        data = [
            Content(parts=[Part(text=mock_chatbot_message_list_dict["messages"][0]["message"])], role="user"),
            Content(parts=[Part(text=mock_chatbot_message_list_dict["messages"][1]["message"])], role="model"),
        ]
        chatbot_message_list = ChatbotMessageList.from_contents_list(data)
        # Patch timestamps
        for i, message in enumerate(chatbot_message_list.messages):
            message.timestamp = mock_chatbot_message_list_dict["messages"][i]["timestamp"]

        assert chatbot_message_list.model_dump() == mock_chatbot_message_list_dict

        history = chatbot_message_list.as_contents_list
        assert history == data


class TestChatbotSpeech:
    """Tests for the ChatbotSpeech class."""

    def test_model_dump(self, mock_chatbot_speech_dict: dict, mock_chatbot_speech: ChatbotSpeech) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_speech.model_dump() == mock_chatbot_speech_dict


# Chatbot Server Configuration Models
class TestChatbotConfig:
    """Unit tests for the TestChatbotConfig class."""

    def test_model_dump(self, mock_chatbot_config_dict: dict, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_config.model_dump() == mock_chatbot_config_dict


class TestChatbotServerConfig:
    """Unit tests for the TestChatbotServerConfig class."""

    def test_model_dump(
        self, mock_chatbot_server_config: ChatbotServerConfig, mock_chatbot_config: ChatbotConfig
    ) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_server_config.chatbot_config.model_dump() == mock_chatbot_config.model_dump()


# Chatbot Server Response Models
class TestGetConfigResponse:
    """Unit tests for the TestGetConfigResponse class."""

    def test_model_dump(self, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the model_dump method."""
        expected_dict = {
            "code": ResponseCode.OK,
            "message": "Config retrieved successfully",
            "timestamp": "2023-01-01T00:00:00Z",
            "config": mock_chatbot_config.model_dump(),
        }
        get_config_response = GetConfigResponse.model_validate(expected_dict)
        assert get_config_response.model_dump() == expected_dict


class TestGetChatHistoryResponse:
    """Unit tests for the TestGetChatHistoryResponse class."""

    def test_model_dump(self, mock_chatbot_message_list: ChatbotMessageList) -> None:
        """Test the model_dump method."""
        expected_dict = {
            "code": ResponseCode.OK,
            "message": "Chat history retrieved successfully",
            "timestamp": "2023-01-01T00:00:00Z",
            "chat_history": mock_chatbot_message_list.model_dump(),
        }
        get_chat_history_response = GetChatHistoryResponse.model_validate(expected_dict)
        assert get_chat_history_response.model_dump() == expected_dict


class TestPostMessageResponse:
    """Unit tests for the TestPostMessageResponse class."""

    def test_model_dump(self, mock_chatbot_message_model: ChatbotMessage) -> None:
        """Test the model_dump method."""
        expected_dict = {
            "code": ResponseCode.OK,
            "message": "Message processed successfully",
            "timestamp": "2023-01-01T00:00:00Z",
            "reply": mock_chatbot_message_model.model_dump(),
        }
        post_message_response = PostMessageResponse.model_validate(expected_dict)
        assert post_message_response.model_dump() == expected_dict


class TestPostAudioResponse:
    """Unit tests for the TestPostAudioResponse class."""

    def test_model_dump(self, mock_chatbot_speech: ChatbotSpeech) -> None:
        """Test the model_dump method."""
        expected_dict = {
            "code": ResponseCode.OK,
            "message": "Audio processed successfully",
            "timestamp": "2023-01-01T00:00:00Z",
            "reply": mock_chatbot_speech.model_dump(),
        }
        post_audio_response = PostAudioResponse.model_validate(expected_dict)
        assert post_audio_response.model_dump() == expected_dict
