import json
from unittest.mock import mock_open, patch

from rpi_ai.types import AIConfigType, Message, SpeechResponse


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
