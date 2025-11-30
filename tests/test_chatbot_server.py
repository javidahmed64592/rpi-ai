"""Unit tests for the rpi_ai.chatbot_server module."""

import asyncio
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
from rpi_ai.models import ChatbotServerConfig


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
def mock_chatbot_server(mock_chatbot_server_config: ChatbotServerConfig) -> Generator[ChatbotServer, None, None]:
    """Provide a ChatbotServer instance for testing."""

    async def fake_verify_api_key(
        api_key: str | None = Security(APIKeyHeader(name="X-API-Key", auto_error=False)),
    ) -> None:
        """Fake verify API key that accepts the security header and always succeeds in tests."""
        return

    with patch.object(ChatbotServer, "_verify_api_key", new=fake_verify_api_key):
        chatbot_server = ChatbotServer(mock_chatbot_server_config)
        yield chatbot_server


class TestChatbotServer:
    """Unit tests for the ChatbotServer class."""

    def test_init(self, mock_chatbot_server: ChatbotServer) -> None:
        """Test ChatbotServer initialization."""
        assert isinstance(mock_chatbot_server.config, ChatbotServerConfig)
        assert isinstance(mock_chatbot_server.chatbot, Chatbot)

    def test_validate_config(
        self, mock_chatbot_server: ChatbotServer, mock_chatbot_server_config: ChatbotServerConfig
    ) -> None:
        """Test configuration validation."""
        config_dict = mock_chatbot_server_config.model_dump()
        validated_config = mock_chatbot_server.validate_config(config_dict)
        assert validated_config == mock_chatbot_server_config

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
            "/metrics",
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
