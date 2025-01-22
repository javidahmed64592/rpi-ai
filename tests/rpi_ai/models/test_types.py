from unittest.mock import MagicMock

from rpi_ai.models.types import Message, MessageList


class TestMessage:
    def test_from_dict_user_message(self, mock_extract_parts: MagicMock) -> None:
        data = {"role": "user", "parts": "Hello, world!"}
        mock_extract_parts.return_value = data["parts"]
        message = Message.from_dict(data)
        assert message.message == "Hello, world!"
        assert message.is_user_message

    def test_from_dict_model_message(self, mock_extract_parts: MagicMock) -> None:
        data = {"role": "model", "parts": "Hello, user!"}
        mock_extract_parts.return_value = data["parts"]
        message = Message.from_dict(data)
        assert message.message == "Hello, user!"
        assert not message.is_user_message


class TestMessageList:
    def test_from_history(self, mock_extract_parts: MagicMock) -> None:
        data = [
            {"role": "user", "parts": "Hello, world!"},
            {"role": "model", "parts": "Hello, user!"},
        ]
        mock_extract_parts.side_effect = [data[0]["parts"], data[1]["parts"]]
        message_list = MessageList.from_history(data)
        assert len(message_list.messages) == len(data)
        assert message_list.messages[0].message == "Hello, world!"
        assert message_list.messages[0].is_user_message
        assert message_list.messages[1].message == "Hello, user!"
        assert not message_list.messages[1].is_user_message
