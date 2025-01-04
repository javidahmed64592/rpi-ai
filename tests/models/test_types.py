from rpi_ai.models.types import Message, MessageList


class TestMessage:
    def test_from_dict_user_message(self) -> None:
        data = {"role": "user", "parts": "Hello, world!"}
        message = Message.from_dict(data)
        assert message.message == "Hello, world!"
        assert message.is_user_message

    def test_from_dict_model_message(self) -> None:
        data = {"role": "model", "parts": "Hello, user!"}
        message = Message.from_dict(data)
        assert message.message == "Hello, user!"
        assert not message.is_user_message


class TestMessageList:
    def test_from_history(self) -> None:
        data = [
            {"role": "user", "parts": "Hello, world!"},
            {"role": "model", "parts": "Hello, user!"},
        ]
        message_list = MessageList.from_history(data)
        assert len(message_list.messages) == 2
        assert message_list.messages[0].message == "Hello, world!"
        assert message_list.messages[0].is_user_message
        assert message_list.messages[1].message == "Hello, user!"
        assert not message_list.messages[1].is_user_message
