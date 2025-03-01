from datetime import datetime

from google.genai.types import Content, Part

from rpi_ai.api_types import Message, MessageList, SpeechResponse


class TestMessage:
    def test_user_message(self) -> None:
        timestamp = int(datetime.now().timestamp())
        message = Message.user_message("test_message", timestamp)
        assert message.message == "test_message"
        assert message.timestamp == timestamp
        assert message.is_user_message

    def test_model_message(self) -> None:
        timestamp = int(datetime.now().timestamp())
        message = Message.model_message("test_message", timestamp)
        assert message.message == "test_message"
        assert message.timestamp == timestamp
        assert not message.is_user_message

    def test_new_chat_message(self) -> None:
        timestamp = int(datetime.now().timestamp())
        message = Message.new_chat_message(timestamp)
        assert message.message == "What's on your mind today?"
        assert message.timestamp == timestamp
        assert not message.is_user_message


class TestMessageList:
    def test_from_contents_list(self) -> None:
        good_data = [
            Content(parts=[Part(text="user_msg")], role="user"),
            Content(parts=[Part(text="model_msg")], role="model"),
        ]
        bad_data = [
            Content(parts=[], role="user"),
        ]
        data = good_data + bad_data
        message_list = MessageList.from_contents_list(data)
        assert len(message_list.messages) == len(good_data)
        assert message_list.messages[0].message == "user_msg"
        assert message_list.messages[0].is_user_message
        assert message_list.messages[1].message == "model_msg"
        assert not message_list.messages[1].is_user_message

    def test_history(self) -> None:
        data = [
            Content(parts=[Part(text="user_msg")], role="user"),
            Content(parts=[Part(text="model_msg")], role="model"),
        ]
        message_list = MessageList.from_contents_list(data)
        history = message_list.as_contents_list
        assert len(history) == len(data)
        assert history[0].parts[0].text == "user_msg"
        assert history[0].role == "user"
        assert history[1].parts[0].text == "model_msg"
        assert history[1].role == "model"


class TestSpeechResponse:
    def test_from_dict(self) -> None:
        timestamp = int(datetime.now().timestamp())
        data = {"bytes": "audio_data", "timestamp": timestamp, "message": "Hello, world!"}
        response = SpeechResponse(**data)
        assert response.message == "Hello, world!"
        assert response.timestamp == timestamp
        assert response.bytes == "audio_data"
