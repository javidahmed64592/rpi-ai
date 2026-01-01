"""Unit tests for the rpi_ai.main module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from rpi_ai.main import run
from rpi_ai.models import ChatbotServerConfig


@pytest.fixture
def mock_chatbot_server_class(mock_chatbot_server_config: ChatbotServerConfig) -> Generator[MagicMock]:
    """Mock ChatbotServer class."""
    with patch("rpi_ai.main.ChatbotServer") as mock_server:
        mock_server.load_config.return_value = mock_chatbot_server_config
        yield mock_server


class TestRun:
    """Unit tests for the run function."""

    def test_run(self, mock_chatbot_server_class: MagicMock) -> None:
        """Test successful server run."""
        run()

        mock_chatbot_server_class.return_value.run.assert_called_once()
