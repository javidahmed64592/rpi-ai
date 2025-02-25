import json
from unittest.mock import mock_open, patch

from google.genai.types import Content, Part

from rpi_ai.api_types import AIConfigType, MessageList, SpeechResponse


# Config
class TestAIConfigType:
    def test_load(self, config_data: dict[str, str | float]) -> None:
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(config_data)):
            config = AIConfigType.load("dummy_path")
            assert config.model == "test-model"
            assert config.candidate_count == config_data["candidate_count"]
            assert config.max_output_tokens == config_data["max_output_tokens"]
            assert config.temperature == config_data["temperature"]

    def test_save(self, config_data: dict[str, str | float]) -> None:
        with patch("builtins.open", new_callable=mock_open) as mock_file:
            config = AIConfigType(**config_data)
            config.save("dummy_path")
            mock_file.assert_called_once_with("dummy_path", "w")
            handle = mock_file()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            assert written_data == json.dumps(config_data, indent=4)


# Chatbot responses
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
        history = message_list.history
        assert len(history) == len(data)
        assert history[0].parts[0].text == "user_msg"
        assert history[0].role == "user"
        assert history[1].parts[0].text == "model_msg"
        assert history[1].role == "model"


class TestSpeechResponse:
    def test_from_dict(self) -> None:
        data = {"message": "Hello, world!", "bytes": "audio_data"}
        response = SpeechResponse(**data)
        assert response.message == "Hello, world!"
        assert response.bytes == "audio_data"
