import json
from unittest.mock import mock_open, patch

from google.genai.types import FunctionCall

from rpi_ai.types import AIConfigType, FunctionTool, FunctionToolList, Message, SpeechResponse


# Config
class TestAIConfigType:
    def test_load(self, config_data: dict[str, str | float]) -> None:
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(config_data)):
            config = AIConfigType.load("dummy_path")
            assert config.model == "test-model"
            assert config.candidate_count == config_data["candidate_count"]
            assert config.max_output_tokens == config_data["max_output_tokens"]
            assert config.temperature == config_data["temperature"]


# Chatbot responses
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


class TestSpeechResponse:
    def test_from_dict(self) -> None:
        data = {"message": "Hello, world!", "bytes": "audio_data"}
        response = SpeechResponse(**data)
        assert response.message == "Hello, world!"
        assert response.bytes == "audio_data"


# Functions
class TestFunctionTool:
    def test_name(self) -> None:
        fn = FunctionCall(name="test_function", args={})
        response = FunctionTool(fn, lambda: {})
        assert response.name == "test_function"

    def test_args(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1", "arg2": "value2"})
        response = FunctionTool(fn, lambda: {})
        assert set(response.args.split(", ")) == {"arg1=value1", "arg2=value2"}

    def test_response_without_args(self) -> None:
        fn = FunctionCall(name="test_function", args={})
        response = FunctionTool(fn, lambda: {"result": "success"})
        assert response.response == {"result": "success"}

    def test_response_with_args(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1"})
        response = FunctionTool(fn, lambda arg1: {"result": f"success with {arg1}"})
        assert response.response == {"result": "success with value1"}

    def test_output(self) -> None:
        fn = FunctionCall(name="test_function", args={"arg1": "value1"})
        response = FunctionTool(fn, lambda arg1: {"result": f"success with {arg1}"})
        assert response.output == "test_function(arg1=value1)={'result': 'success with value1'}"


class TestFunctionToolList:
    def test_dictionary(self) -> None:
        def fn1() -> None:
            return "fn1"

        def fn2() -> None:
            return "fn2"

        functions_list = FunctionToolList([fn1, fn2])
        assert functions_list.dictionary == {"fn1": fn1, "fn2": fn2}
        assert functions_list["fn1"]() == "fn1"
        assert functions_list["fn2"]() == "fn2"
