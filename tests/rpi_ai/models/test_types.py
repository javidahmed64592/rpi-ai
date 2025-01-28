from unittest.mock import MagicMock

from google.generativeai.protos import FunctionCall

from rpi_ai.models.types import CallableFunctionResponse, FunctionsList, Message, MessageList


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


class TestFunctionResponse:
    def test_name(self) -> None:
        fn = FunctionCall(name="test_function", args={})
        response = CallableFunctionResponse(fn, lambda: {})
        assert response.name == "test_function"

    def test_args(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1", "arg2": "value2"})
        response = CallableFunctionResponse(fn, lambda: {})
        assert set(response.args.split(", ")) == {"arg1=value1", "arg2=value2"}

    def test_response_without_args(self) -> None:
        fn = FunctionCall(name="test_function", args={})
        response = CallableFunctionResponse(fn, lambda: {"result": "success"})
        assert response.response == {"result": "success"}

    def test_response_with_args(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1"})
        response = CallableFunctionResponse(fn, lambda arg1: {"result": f"success with {arg1}"})
        assert response.response == {"result": "success with value1"}

    def test_output(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1"})
        response = CallableFunctionResponse(fn, lambda arg1: {"result": f"success with {arg1}"})
        assert response.output == "test_function(arg1=value1)={'result': 'success with value1'}"


class TestFunctionsList:
    def test_dictionary(self) -> None:
        def fn1() -> None:
            pass

        def fn2() -> None:
            pass

        functions_list = FunctionsList([fn1, fn2])
        assert functions_list.dictionary == {"fn1": fn1, "fn2": fn2}

    def test_getitem(self) -> None:
        def fn1() -> None:
            pass

        def fn2() -> None:
            pass

        functions_list = FunctionsList([fn1, fn2])
        assert functions_list["fn1"] == fn1
        assert functions_list["fn2"] == fn2
