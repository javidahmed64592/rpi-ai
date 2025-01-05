from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from flask import Flask

from rpi_ai.main import AIApp
from rpi_ai.models.types import Message, MessageList


@pytest.fixture
def config_data() -> dict[str, str | float]:
    return {"model": "test-model", "candidate_count": 2, "max_output_tokens": 50, "temperature": 0.7}


@pytest.fixture
def mock_chat_history() -> MessageList:
    return MessageList([Message("Hello, World!")])


@pytest.fixture
def mock_ai_app(mock_chatbot: MagicMock) -> AIApp:
    return AIApp()


@pytest.fixture
def mock_client(mock_ai_app: AIApp) -> Generator[Flask, None, None]:
    mock_ai_app.app.config["TESTING"] = True
    with mock_ai_app.app.test_client() as client:
        yield client
