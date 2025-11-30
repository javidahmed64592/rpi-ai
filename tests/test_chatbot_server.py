"""Unit tests for the rpi_ai.chatbot_server module."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.routing import APIRoute
from python_template_server.constants import CONFIG_DIR

from rpi_ai.chatbot import Chatbot
from rpi_ai.chatbot_server import ChatbotServer
from rpi_ai.models import ChatbotServerConfig


@pytest.fixture
def mock_chatbot_server(mock_chatbot_server_config: ChatbotServerConfig) -> ChatbotServer:
    """Provide a ChatbotServer instance for testing."""
    return ChatbotServer(mock_chatbot_server_config)


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
