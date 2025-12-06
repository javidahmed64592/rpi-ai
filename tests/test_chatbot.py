"""Unit tests for the rpi_ai.chatbot module."""

from unittest.mock import MagicMock

import pytest
from google.genai.errors import ServerError
from google.genai.types import GenerateContentConfig, GoogleSearch
from gtts import gTTSError

from rpi_ai.chatbot import Chatbot
from rpi_ai.models import ChatbotConfig


class TestChatbot:
    """Tests for the Chatbot class."""

    def test_init(self, mock_chatbot: Chatbot, mock_env_vars: MagicMock, mock_genai_client: MagicMock) -> None:
        """Test initialisation of the Chatbot class."""
        mock_genai_client.assert_called_once_with(api_key=mock_env_vars["GEMINI_API_KEY"])

    def test_model_config(self, mock_chatbot: Chatbot, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the model configuration of the Chatbot."""
        config = mock_chatbot._model_config
        assert (
            config.system_instruction
            == f"{mock_chatbot_config.system_instruction}\n{ChatbotConfig.get_memory_guidelines()}"
        )
        assert config.max_output_tokens == mock_chatbot_config.max_output_tokens
        assert config.temperature == mock_chatbot_config.temperature
        assert config.safety_settings == mock_chatbot.SAFETY_SETTINGS
        assert config.candidate_count == mock_chatbot.CANDIDATE_COUNT

    def test_chat_config(self, mock_chatbot: Chatbot, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the chat configuration of the Chatbot."""
        config = mock_chatbot._chat_config
        assert (
            config.system_instruction
            == f"{mock_chatbot_config.system_instruction}\n{ChatbotConfig.get_memory_guidelines()}"
        )
        assert config.max_output_tokens == mock_chatbot_config.max_output_tokens
        assert config.temperature == mock_chatbot_config.temperature
        assert config.safety_settings == mock_chatbot.SAFETY_SETTINGS
        assert config.candidate_count == mock_chatbot.CANDIDATE_COUNT
        assert isinstance(config.tools, list)
        assert len(config.tools) > 0
        assert config.tools[0] in mock_chatbot._functions

    def test_web_search_config(self, mock_chatbot: Chatbot, mock_chatbot_config: ChatbotConfig) -> None:
        """Test the web search configuration of the Chatbot."""
        config = mock_chatbot._web_search_config
        assert (
            config.system_instruction
            == f"{mock_chatbot_config.system_instruction}\n{ChatbotConfig.get_memory_guidelines()}"
        )
        assert config.max_output_tokens == mock_chatbot_config.max_output_tokens
        assert config.temperature == mock_chatbot_config.temperature
        assert config.safety_settings == mock_chatbot.SAFETY_SETTINGS
        assert config.candidate_count == mock_chatbot.CANDIDATE_COUNT
        assert isinstance(config.tools, list)
        assert len(config.tools) == 1
        assert config.tools[0].google_search == GoogleSearch()

    def test_chat_history(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        """Test the chat history of the Chatbot."""
        history = mock_chatbot.chat_history
        assert len(history.messages) == 1
        assert history.messages[0].message == "What's on your mind today?"

    def test_embed_text(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test embedding text with the default task type."""
        mock_vector = [0.1, 0.2, 0.3]
        mock_embedding_response = MagicMock(embeddings=[MagicMock(values=mock_vector)])
        mock_genai_client.return_value.models.embed_content.return_value = mock_embedding_response

        result = mock_chatbot._embed_text("test text", task_type="SEMANTIC_SIMILARITY")
        mock_genai_client.return_value.models.embed_content.assert_called_once()
        assert result.tolist() == mock_vector

    def test_embed_text_no_embeddings(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test embedding text when no embeddings are returned."""
        mock_embedding_response = MagicMock(embeddings=[])
        mock_genai_client.return_value.models.embed_content.return_value = mock_embedding_response

        with pytest.raises(AttributeError, match=r"No embeddings returned from embedding model."):
            mock_chatbot._embed_text("test text", task_type="SEMANTIC_SIMILARITY")

    def test_create_memory(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test creating a new memory entry."""
        mock_vector = [0.1, 0.2, 0.3]
        mock_embedding_response = MagicMock(embeddings=[MagicMock(values=mock_vector)])
        mock_genai_client.return_value.models.embed_content.return_value = mock_embedding_response

        initial_count = len(mock_chatbot._memory.entries)
        memory_text = "New memory"

        response = mock_chatbot.create_memory(memory_text)
        assert response == f"Memory stored successfully: {memory_text}"

        assert len(mock_chatbot._memory.entries) == initial_count + 1
        assert mock_chatbot._memory.entries[-1].text == memory_text
        assert mock_chatbot._memory.entries[-1].vector == mock_vector
        mock_genai_client.return_value.models.embed_content.assert_called_once()

    def test_retrieve_memories(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test retrieving relevant memories based on a query."""
        mock_vector = [0.1, 0.2, 0.3]
        mock_embedding_response = MagicMock(embeddings=[MagicMock(values=mock_vector)])
        mock_genai_client.return_value.models.embed_content.return_value = mock_embedding_response

        query = "What music do I like?"
        memories = mock_chatbot.retrieve_memories(query)

        assert isinstance(memories, list)
        assert all(isinstance(memory, str) for memory in memories)
        mock_genai_client.return_value.models.embed_content.assert_called_once()

    def test_retrieve_memories_returns_top_k(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test that retrieve_memories returns at most top_k results."""
        # Add multiple memory entries with non-zero vectors
        for i in range(5):
            mock_chatbot._memory.entries.append(
                MagicMock(text=f"Memory {i}", vector=[0.1 * (i + 1), 0.2 * (i + 1), 0.3 * (i + 1)])
            )

        mock_embedding_response = MagicMock(embeddings=[MagicMock(values=[0.5, 0.5, 0.5])])
        mock_genai_client.return_value.models.embed_content.return_value = mock_embedding_response

        memories = mock_chatbot.retrieve_memories("test query")

        assert len(memories) <= mock_chatbot._embedding_config.top_k
        mock_genai_client.return_value.models.embed_content.assert_called_once()

    def test_clear_memories(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test clearing all stored chat memories."""
        assert len(mock_chatbot._memory.entries) > 0

        mock_chatbot.clear_memories()

        assert len(mock_chatbot._memory.entries) == 0

    def test_web_search(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test the web search functionality of the Chatbot."""
        query = "test query"
        mock_response = MagicMock(text="search results")
        mock_genai_client.return_value.models.generate_content.return_value = mock_response

        result = mock_chatbot.web_search(query)
        mock_genai_client.return_value.models.generate_content.assert_called_once_with(
            contents=query,
            model=mock_chatbot._config.model,
            config=mock_chatbot._web_search_config,
        )
        assert result == "search results"

    def test_extract_blocked_categories(self, mock_chatbot: Chatbot) -> None:
        """Test the extraction of blocked categories from a response."""
        mock_response = MagicMock(candidates=[MagicMock(safety_ratings=[MagicMock(blocked=True, category="test")])])
        blocked_categories = mock_chatbot._extract_blocked_categories(mock_response)
        assert blocked_categories == ["test"]

    def test_handle_blocked_message(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        """Test handling a blocked message."""
        mock_chat_instance.send_message.return_value = MagicMock(text="Blocked message")
        blocked_categories = ["test"]
        blocked_categories_str = ", ".join(blocked_categories)
        response = mock_chatbot._handle_blocked_message(blocked_categories)
        mock_chat_instance.send_message.assert_called_with(
            f"The previous message was blocked because it violates the following categories: {blocked_categories_str}."
        )
        assert response == "Blocked message"

    def test_get_config(self, mock_chatbot: Chatbot, mock_chatbot_config: ChatbotConfig) -> None:
        """Test retrieving the configuration of the Chatbot."""
        assert mock_chatbot.get_config() == mock_chatbot_config

    def test_update_config(self, mock_chatbot: Chatbot, mock_chatbot_config: ChatbotConfig) -> None:
        """Test updating the configuration of the Chatbot."""
        mock_chatbot_config.model = "new-model"
        mock_chatbot.update_config(mock_chatbot_config)
        assert mock_chatbot.get_config() == mock_chatbot_config

    def test_start_chat(self, mock_chatbot: Chatbot, mock_genai_client: MagicMock) -> None:
        """Test starting a new chat session."""
        mock_genai_client.return_value.chats.create.assert_called_once_with(
            model=mock_chatbot._config.model,
            config=GenerateContentConfig(
                system_instruction=f"{mock_chatbot._config.system_instruction}\n{ChatbotConfig.get_memory_guidelines()}",
                max_output_tokens=mock_chatbot._config.max_output_tokens,
                temperature=mock_chatbot._config.temperature,
                safety_settings=Chatbot.SAFETY_SETTINGS,
                candidate_count=1,
                tools=mock_chatbot._functions,
            ),
        )
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_send_message_with_valid_response(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        """Test sending a message with a valid response."""
        mock_msg = "Hi model!"
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)

        assert mock_chatbot.chat_history.messages[-2].message == mock_msg
        assert mock_chatbot.chat_history.messages[-2].is_user_message

        assert mock_chatbot.chat_history.messages[-1].message == response.message
        assert not mock_chatbot.chat_history.messages[-1].is_user_message

    def test_send_message_with_no_response(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        """Test sending a message when no response is received from the model."""
        mock_msg = "Hi model!"
        mock_chat_instance.send_message.return_value = MagicMock(text="")
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "Failed to send message to chatbot!"
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_send_message_with_blocked_response(
        self,
        mock_chatbot: Chatbot,
        mock_chat_instance: MagicMock,
    ) -> None:
        """Test sending a message that results in a blocked response."""
        mock_msg = "Hi model!"
        mock_responses = [
            MagicMock(candidates=[MagicMock(text=None, safety_ratings=[MagicMock(blocked=True, category=["test"])])]),
            MagicMock(text="Blocked message"),
        ]
        mock_chat_instance.send_message.side_effect = mock_responses

        response = mock_chatbot.send_message(mock_msg)
        assert response.message == "Blocked message"
        assert len(mock_chatbot.chat_history.messages) == 1 + 2

    def test_send_message_with_server_error(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        """Test sending a message when a server error occurs."""
        mock_msg = "Hi model!"
        mock_chat_instance.send_message.side_effect = ServerError(
            code=503,
            response_json={"error": {"message": "Model overloaded!"}},
            response=MagicMock(body_segments=[{"error": {"message": "Model overloaded!"}}]),
        )

        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "Model overloaded! Please try again."
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_send_audio_with_valid_response(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        """Test sending an audio message with a valid response."""
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        mock_audio = "test_audio_response"
        mock_get_audio_bytes_from_text.return_value = mock_audio
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()

        assert mock_chatbot.chat_history.messages[-2].message == "Respond to the voice message."
        assert mock_chatbot.chat_history.messages[-2].is_user_message

        assert mock_chatbot.chat_history.messages[-1].message == response.message
        assert not mock_chatbot.chat_history.messages[-1].is_user_message

    def test_send_audio_with_no_response(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        """Test sending an audio message when no response is received from the model."""
        mock_chat_instance.send_message.return_value = MagicMock(parts=MagicMock(text=None))

        mock_audio = "Failed to send messages to chatbot!"
        mock_get_audio_bytes_from_text.return_value = mock_audio

        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Failed to send audio to chatbot!"
        assert response.bytes == mock_audio
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_send_audio_with_blocked_response(
        self,
        mock_chatbot: Chatbot,
        mock_chat_instance: MagicMock,
        mock_get_audio_bytes_from_text: MagicMock,
    ) -> None:
        """Test sending an audio message that results in a blocked response."""
        mock_responses = [
            MagicMock(candidates=[MagicMock(text=None, safety_ratings=[MagicMock(blocked=True, category=["test"])])]),
            MagicMock(text="Blocked message"),
        ]
        mock_chat_instance.send_message.side_effect = mock_responses

        mock_audio = "Blocked message audio"
        mock_get_audio_bytes_from_text.return_value = mock_audio

        response = mock_chatbot.send_audio(b"test_audio_data")
        assert response.message == "Blocked message"
        assert response.bytes == mock_audio
        assert len(mock_chatbot.chat_history.messages) == 1 + 2

    def test_send_audio_with_server_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        """Test sending an audio message when a server error occurs."""
        mock_chat_instance.send_message.side_effect = ServerError(
            code=503,
            response_json={"error": {"message": "Model overloaded!"}},
            response=MagicMock(body_segments=[{"error": {"message": "Model overloaded!"}}]),
        )

        mock_audio = "Model overloaded! Please try again."
        mock_get_audio_bytes_from_text.return_value = mock_audio

        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Model overloaded! Please try again."
        assert response.bytes == mock_audio
        assert len(mock_chatbot.chat_history.messages) == 1

    def test_send_audio_with_gtts_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        """Test sending an audio message when gTTS raises an error."""
        mock_chat_instance.send_message.return_value = MagicMock(text="Hi user!")
        mock_get_audio_bytes_from_text.side_effect = gTTSError("gTTS error")

        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "gTTS error"
        assert response.bytes == ""
        assert len(mock_chatbot.chat_history.messages) == 1
