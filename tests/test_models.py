"""Unit tests for the rpi_ai.models module."""

from datetime import datetime

from google.genai.types import Content, Part

from rpi_ai.models import ChatbotMessage, ChatbotMessageList, ChatbotSpeech


class TestChatbotMessage:
    """Tests for the ChatbotMessage class."""

    def test_user_message(self) -> None:
        """Test creating a user message."""
        timestamp = int(datetime.now().timestamp())
        message = ChatbotMessage.user_message("test_message", timestamp)
        assert message.message == "test_message"
        assert message.timestamp == timestamp
        assert message.is_user_message

    def test_model_message(self) -> None:
        """Test creating a model message."""
        timestamp = int(datetime.now().timestamp())
        message = ChatbotMessage.model_message("test_message", timestamp)
        assert message.message == "test_message"
        assert message.timestamp == timestamp
        assert not message.is_user_message

    def test_new_chat_message(self) -> None:
        """Test creating a new chat message."""
        timestamp = int(datetime.now().timestamp())
        message = ChatbotMessage.new_chat_message(timestamp)
        assert message.message == "What's on your mind today?"
        assert message.timestamp == timestamp
        assert not message.is_user_message


class TestChatbotMessageList:
    """Tests for the ChatbotMessageList class."""

    def test_from_contents_list(self) -> None:
        """Test creating a ChatbotMessageList from a list of Content."""
        good_data = [
            Content(parts=[Part(text="user_msg")], role="user"),
            Content(parts=[Part(text="model_msg")], role="model"),
        ]
        bad_data = [
            Content(parts=[], role="user"),
        ]
        data = good_data + bad_data
        message_list = ChatbotMessageList.from_contents_list(data)
        assert len(message_list.messages) == len(good_data)
        assert message_list.messages[0].message == "user_msg"
        assert message_list.messages[0].is_user_message
        assert message_list.messages[1].message == "model_msg"
        assert not message_list.messages[1].is_user_message

    def test_history(self) -> None:
        """Test converting a ChatbotMessageList to a history list."""
        data = [
            Content(parts=[Part(text="user_msg")], role="user"),
            Content(parts=[Part(text="model_msg")], role="model"),
        ]
        message_list = ChatbotMessageList.from_contents_list(data)
        history = message_list.as_contents_list
        assert len(history) == len(data)
        assert isinstance(history, list)
        assert isinstance(history[0].parts, list)
        assert history[0].parts[0].text == "user_msg"
        assert history[0].role == "user"
        assert isinstance(history[1].parts, list)
        assert history[1].parts[0].text == "model_msg"
        assert history[1].role == "model"


class TestChatbotSpeech:
    """Tests for the ChatbotSpeech class."""

    def test_from_dict(self) -> None:
        """Test creating a ChatbotSpeech from a dictionary."""
        timestamp = int(datetime.now().timestamp())
        data = {"bytes": "audio_data", "timestamp": timestamp, "message": "Hello, world!"}
        response = ChatbotSpeech.model_validate(data)
        assert response.message == "Hello, world!"
        assert response.timestamp == timestamp
        assert response.bytes == "audio_data"
