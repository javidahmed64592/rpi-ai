"""Unit tests for the rpi_ai.models module."""

from pathlib import Path
from unittest.mock import MagicMock

from google.genai.types import Content, Part
from python_template_server.models import ResponseCode

from rpi_ai.models import (
    ChatbotConfig,
    ChatbotMessage,
    ChatbotMessageList,
    ChatbotServerConfig,
    ChatbotSpeech,
    ChatMemoryEntry,
    ChatMemoryList,
    EmbeddingConfig,
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


# Memory Models
class TestChatMemoryEntry:
    """Tests for the ChatMemoryEntry class."""

    def test_model_dump(self, mock_chat_memory_entry_dict: dict, mock_chat_memory_entry: ChatMemoryEntry) -> None:
        """Test the model_dump method."""
        assert mock_chat_memory_entry.model_dump() == mock_chat_memory_entry_dict


class TestChatMemoryList:
    """Tests for the ChatMemoryList class."""

    def test_model_dump(self, mock_chat_memory_list: ChatMemoryList, mock_chat_memory_entry: ChatMemoryEntry) -> None:
        """Test the model_dump method."""
        assert mock_chat_memory_list.model_dump() == {"entries": [mock_chat_memory_entry.model_dump()]}

    def test_add_entry(self, mock_chat_memory_list: ChatMemoryList) -> None:
        """Test adding an entry to the ChatMemoryList."""
        new_entry = ChatMemoryEntry(text="Another memory entry", vector=[0.4, 0.5, 0.6])
        mock_chat_memory_list.add_entry(text=new_entry.text, vector=new_entry.vector)
        latest_entry = mock_chat_memory_list.entries[-1]
        assert latest_entry.text == new_entry.text
        assert latest_entry.vector == new_entry.vector

    def test_clear_entries(self, mock_chat_memory_list: ChatMemoryList) -> None:
        """Test clearing entries from the ChatMemoryList."""
        mock_chat_memory_list.clear_entries()
        assert mock_chat_memory_list.entries == []

    def test_retrieve_memories(self, mock_chat_memory_list: ChatMemoryList) -> None:
        """Test retrieving similar memories from the ChatMemoryList."""
        new_entry = mock_chat_memory_list.entries[0].model_copy()
        new_entry.text = "Modified memory entry"
        new_entry.vector = [component + 0.01 for component in new_entry.vector]

        mock_chat_memory_list.add_entry(text=new_entry.text, vector=new_entry.vector)
        top_memories = mock_chat_memory_list.retrieve_memories(new_entry.vector, top_k=1)
        assert top_memories == [new_entry.text]

    def test_save_to_file(
        self, mock_chat_memory_list: ChatMemoryList, mock_open_file: MagicMock, mock_json_dump: MagicMock
    ) -> None:
        """Test saving ChatMemoryList to a file."""
        file_path = Path("chat_memory.json")
        mock_chat_memory_list.save_to_file(file_path)
        mock_open_file.assert_called_once_with("w")
        mock_json_dump.assert_called_once_with(mock_chat_memory_list.model_dump(), mock_open_file(), indent=2)

    def test_load_from_file(
        self, mock_chat_memory_list: ChatMemoryList, mock_open_file: MagicMock, mock_json_load: MagicMock
    ) -> None:
        """Test loading ChatMemoryList from a file."""
        file_path = Path("chat_memory.json")
        mock_json_load.return_value = mock_chat_memory_list.model_dump()

        loaded_memory_list = ChatMemoryList.load_from_file(file_path)
        mock_open_file.assert_called_once_with()
        mock_json_load.assert_called_once_with(mock_open_file())
        assert loaded_memory_list.model_dump() == mock_chat_memory_list.model_dump()

    def test_load_from_file_file_not_found(self, mock_open_file: MagicMock, mock_json_load: MagicMock) -> None:
        """Test loading ChatMemoryList from a file."""
        file_path = Path("chat_memory.json")
        mock_open_file.side_effect = FileNotFoundError

        loaded_memory_list = ChatMemoryList.load_from_file(file_path)
        mock_open_file.assert_called_once_with()
        mock_json_load.assert_not_called()
        assert loaded_memory_list.entries == []


# Chatbot Server Configuration Models
class TestChatbotConfig:
    """Unit tests for the TestChatbotConfig class."""

    def test_model_dump(self, mock_chatbot_config_dict: dict, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the model_dump method."""
        assert mock_chatbot_config.model_dump() == mock_chatbot_config_dict

    def test_get_memory_guidelines(self) -> None:
        """Test the get_memory_guidelines method."""
        assert "MEMORY GUIDELINES:" in ChatbotConfig.get_memory_guidelines()


class TestEmbeddingConfig:
    """Unit tests for the TestEmbeddingConfig class."""

    def test_model_dump(self, mock_embedding_config_dict: dict, mock_embedding_config: EmbeddingConfig) -> None:
        """Test the model_dump method."""
        assert mock_embedding_config.model_dump() == mock_embedding_config_dict


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
