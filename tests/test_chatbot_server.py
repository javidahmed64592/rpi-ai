"""Unit tests for the rpi_ai.chatbot_server module."""

import asyncio
import json
from collections.abc import Generator
from importlib.metadata import PackageMetadata
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request, Security
from fastapi.routing import APIRoute
from fastapi.security import APIKeyHeader
from fastapi.testclient import TestClient
from python_template_server.constants import CONFIG_DIR
from python_template_server.models import ResponseCode

from rpi_ai.chatbot import Chatbot
from rpi_ai.chatbot_server import ChatbotServer
from rpi_ai.models import ChatbotMessage, ChatbotServerConfig, ChatbotSpeech


@pytest.fixture(autouse=True)
def mock_package_metadata() -> Generator[MagicMock, None, None]:
    """Mock importlib.metadata.metadata to return a mock PackageMetadata."""
    with patch("python_template_server.template_server.metadata") as mock_metadata:
        mock_pkg_metadata = MagicMock(spec=PackageMetadata)
        metadata_dict = {
            "Name": "rpi-ai",
            "Version": "0.1.0",
            "Summary": "A lightweight AI chatbot using Google Gemini.",
        }
        mock_pkg_metadata.__getitem__.side_effect = lambda key: metadata_dict[key]
        mock_metadata.return_value = mock_pkg_metadata
        yield mock_metadata


@pytest.fixture
def mock_chatbot_server(
    mock_chatbot_server_config: ChatbotServerConfig, mock_chatbot: Chatbot
) -> Generator[ChatbotServer, None, None]:
    """Provide a ChatbotServer instance for testing."""

    async def fake_verify_api_key(
        api_key: str | None = Security(APIKeyHeader(name="X-API-Key", auto_error=False)),
    ) -> None:
        """Fake verify API key that accepts the security header and always succeeds in tests."""
        return

    with (
        patch.object(ChatbotServer, "_verify_api_key", new=fake_verify_api_key),
        patch("rpi_ai.chatbot_server.Chatbot", return_value=mock_chatbot),
    ):
        chatbot_server = ChatbotServer(mock_chatbot_server_config)
        yield chatbot_server


class TestChatbotServer:
    """Unit tests for the ChatbotServer class."""

    def test_init(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test ChatbotServer initialization."""
        assert isinstance(mock_chatbot_server.config, ChatbotServerConfig)
        assert isinstance(mock_chatbot_server.chatbot, Chatbot)

    def test_init_missing_api_key(
        self, mock_chatbot_server_config: ChatbotServerConfig, mock_env_vars: MagicMock
    ) -> None:
        """Test ChatbotServer initialization raises ValueError when API key is missing."""
        mock_env_vars["GEMINI_API_KEY"] = ""
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            ChatbotServer(mock_chatbot_server_config)

    def test_validate_config(
        self, mock_chatbot_server: ChatbotServer, mock_chatbot_server_config: ChatbotServerConfig
    ) -> None:
        """Test configuration validation."""
        config_dict = mock_chatbot_server_config.model_dump()
        validated_config = mock_chatbot_server.validate_config(config_dict)
        assert validated_config == mock_chatbot_server_config

    def test_validate_config_invalid_returns_default(
        self, mock_chatbot_server: ChatbotServer, mock_chatbot_server_config: ChatbotServerConfig
    ) -> None:
        """Test invalid configuration returns default configuration."""
        mock_chatbot_server_config.chatbot_config = None  # type: ignore[assignment]
        config_dict = mock_chatbot_server_config.model_dump()
        validated_config = mock_chatbot_server.validate_config(config_dict)
        assert validated_config == ChatbotServerConfig.model_validate({})

    def test_config_dir_home(
        self, mock_chatbot_server: ChatbotServer, mock_exists: MagicMock, mock_path_home: MagicMock
    ) -> None:
        """Test that config_dir returns the home config path when it exists."""
        mock_exists.return_value = True
        mock_path_home.return_value = Path("~")
        assert mock_chatbot_server.config_dir == Path("~") / ".config" / "rpi_ai"

    def test_config_dir_default(self, mock_chatbot_server: ChatbotServer, mock_exists: MagicMock) -> None:
        """Test that config_dir returns the default CONFIG_DIR when home config path does not exist."""
        mock_exists.return_value = False
        assert mock_chatbot_server.config_dir == CONFIG_DIR


class TestChatbotServerRoutes:
    """Integration tests for the routes in ChatbotServer."""

    def test_setup_routes(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test that routes are set up correctly."""
        api_routes = [route for route in mock_chatbot_server.app.routes if isinstance(route, APIRoute)]
        routes = [route.path for route in api_routes]
        expected_endpoints = [
            "/health",
            "/login",
            "/config",
            "/chat/history",
            "/chat/restart",
            "/chat/message",
            "/chat/audio",
        ]
        for endpoint in expected_endpoints:
            assert endpoint in routes


class TestConfigEndpoint:
    """Integration tests for the /config endpoint."""

    def test_get_config(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /config endpoint method."""
        request = MagicMock(spec=Request)
        response = asyncio.run(mock_chatbot_server.get_config(request))

        assert response.code == ResponseCode.OK
        assert response.message == "Successfully retrieved chatbot configuration."
        assert isinstance(response.timestamp, str)
        assert response.config == mock_chatbot_server.chatbot.get_config()

    def test_post_config(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /config POST endpoint method."""
        request = MagicMock(spec=Request)
        new_config = mock_chatbot_server.chatbot.get_config()
        new_config.temperature += 0.1
        request.json = AsyncMock(return_value=new_config.model_dump())
        asyncio.run(mock_chatbot_server.post_config(request))

        updated_config = mock_chatbot_server.chatbot.get_config()
        assert updated_config == new_config

    def test_get_config_endpoint(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test /config endpoint returns 200."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        response = client.get("/config")
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["code"] == ResponseCode.OK
        assert response_body["message"] == "Successfully retrieved chatbot configuration."
        assert isinstance(response_body["timestamp"], str)
        assert response_body["config"] == mock_chatbot_server.chatbot.get_config().model_dump()

    def test_post_config_endpoint(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test /config POST endpoint updates configuration."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        new_config = mock_chatbot_server.chatbot.get_config()
        new_config.temperature += 0.1

        response = client.post("/config", json=new_config.model_dump())
        assert response.status_code == ResponseCode.OK

        updated_config = mock_chatbot_server.chatbot.get_config()
        assert updated_config == new_config


class TestChatHistoryEndpoint:
    """Integration tests for the /chat/history endpoint."""

    def test_get_chat_history(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/history endpoint method."""
        request = MagicMock(spec=Request)
        response = asyncio.run(mock_chatbot_server.get_chat_history(request))

        assert response.code == ResponseCode.OK
        assert response.message == "Successfully retrieved chatbot conversation history."
        assert isinstance(response.timestamp, str)
        assert response.chat_history == mock_chatbot_server.chatbot.chat_history

    def test_get_chat_history_endpoint(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test /chat/history endpoint returns 200."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        response = client.get("/chat/history")
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["code"] == ResponseCode.OK
        assert response_body["message"] == "Successfully retrieved chatbot conversation history."
        assert isinstance(response_body["timestamp"], str)
        assert response_body["chat_history"] == mock_chatbot_server.chatbot.chat_history.model_dump()


class TestRestartChatEndpoint:
    """Integration tests for the /chat/restart endpoint."""

    def test_post_restart_chat(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/restart endpoint method."""
        request = MagicMock(spec=Request)
        asyncio.run(mock_chatbot_server.post_restart_chat(request))

        # Verify that the chat history is reset
        assert len(mock_chatbot_server.chatbot.chat_history.messages) == 1

    def test_post_restart_chat_endpoint(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test /chat/restart endpoint returns 200."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        response = client.post("/chat/restart")
        assert response.status_code == ResponseCode.OK

        # Verify that the chat history is reset
        assert len(mock_chatbot_server.chatbot.chat_history.messages) == 1


class TestPostMessageEndpoint:
    """Integration and unit tests for the /chat/message endpoint."""

    def test_post_message_text(self, mock_chatbot_server: ChatbotServer, mock_chat_instance: MagicMock) -> None:
        """Test the /chat/message method handles valid JSON and returns a model reply."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value={"message": "Hello model!"})
        mock_chat_instance.send_message.return_value = MagicMock(text="Hi user!")
        response = asyncio.run(mock_chatbot_server.post_message_text(request))

        assert response.code == ResponseCode.OK
        assert response.message == "Message sent successfully"
        assert isinstance(response.timestamp, str)
        assert isinstance(response.reply, ChatbotMessage)

    def test_post_message_text_invalid_json(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/message method handles invalid JSON."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(side_effect=json.JSONDecodeError("Expecting value", "", 0))
        response = asyncio.run(mock_chatbot_server.post_message_text(request))

        assert response.code == ResponseCode.BAD_REQUEST
        assert "Invalid JSON" in response.message

    def test_post_message_text_missing_message(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/message method handles missing message in JSON."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value={})
        response = asyncio.run(mock_chatbot_server.post_message_text(request))

        assert response.code == ResponseCode.BAD_REQUEST
        assert "No message provided" in response.message

    def test_post_message_text_endpoint(
        self, mock_chatbot_server: ChatbotServer, mock_chat_instance: MagicMock
    ) -> None:
        """Test /chat/message endpoint returns 200 and includes reply."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        mock_chat_instance.send_message.return_value = MagicMock(text="Hi user!")
        response = client.post("/chat/message", json={"message": "Hello model!"})
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["code"] == ResponseCode.OK
        assert response_body["message"] == "Message sent successfully"
        assert isinstance(response_body["timestamp"], str)
        assert isinstance(response_body["reply"], dict)
        assert response_body["reply"]["message"] == mock_chatbot_server.chatbot.chat_history.messages[-1].message


class TestPostAudioEndpoint:
    """Integration and unit tests for the /chat/audio endpoint."""

    def test_post_message_audio(
        self,
        mock_chatbot_server: ChatbotServer,
        mock_chat_instance: MagicMock,
        mock_get_audio_bytes_from_text: MagicMock,
    ) -> None:
        """Test the /chat/audio method handles a valid audio file and returns a speech response."""
        request = MagicMock(spec=Request)
        file_mock = MagicMock()
        file_mock.read = AsyncMock(return_value=b"sound-bytes")
        request.form = AsyncMock(return_value={"audio": file_mock})
        mock_chat_instance.send_message.return_value = MagicMock(text="Hi user!")
        mock_get_audio_bytes_from_text.return_value = "test_audio_response"
        response = asyncio.run(mock_chatbot_server.post_message_audio(request))

        assert response.code == ResponseCode.OK
        assert response.message == "Audio processed successfully"
        assert isinstance(response.timestamp, str)
        assert isinstance(response.reply, ChatbotSpeech)

    def test_post_message_audio_invalid_form(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/audio method handles invalid form data."""
        request = MagicMock(spec=Request)
        request.form = AsyncMock(side_effect=Exception("form parse failed"))
        response = asyncio.run(mock_chatbot_server.post_message_audio(request))

        assert response.code == ResponseCode.BAD_REQUEST
        assert "Failed to parse form data" in response.message

    def test_post_message_audio_no_file(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/audio method handles missing audio file."""
        request = MagicMock(spec=Request)
        request.form = AsyncMock(return_value={})
        response = asyncio.run(mock_chatbot_server.post_message_audio(request))

        assert response.code == ResponseCode.BAD_REQUEST
        assert "No audio file provided" in response.message

    def test_post_message_audio_read_error(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test the /chat/audio method handles audio read errors."""
        request = MagicMock(spec=Request)
        file_mock = MagicMock()
        file_mock.read = AsyncMock(side_effect=Exception("read failed"))
        request.form = AsyncMock(return_value={"audio": file_mock})
        response = asyncio.run(mock_chatbot_server.post_message_audio(request))

        assert response.code == ResponseCode.BAD_REQUEST
        assert "Failed to read audio file" in response.message

    def test_post_message_audio_endpoint(
        self,
        mock_chatbot_server: ChatbotServer,
        mock_chat_instance: MagicMock,
        mock_get_audio_bytes_from_text: MagicMock,
    ) -> None:
        """Test /chat/audio endpoint returns 200 when uploading a file."""
        app = mock_chatbot_server.app
        client = TestClient(app)

        # Use multipart/form-data with a file field named 'audio'
        files = {"audio": ("audio.wav", b"sound-bytes", "audio/wav")}
        mock_chat_instance.send_message.return_value = MagicMock(text="Hi audio!")
        mock_get_audio_bytes_from_text.return_value = "audio-bytes"
        response = client.post("/chat/audio", files=files)
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["code"] == ResponseCode.OK
        assert response_body["message"] == "Audio processed successfully"
        assert isinstance(response_body["timestamp"], str)
        assert isinstance(response_body["reply"], dict)
