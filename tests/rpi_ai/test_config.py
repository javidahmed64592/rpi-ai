"""Unit tests for the rpi_ai.config module."""

import json
import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from rpi_ai.config import ChatbotConfig, Config


@pytest.fixture
def mock_pathlib_open() -> Generator[MagicMock, None, None]:
    """Mock the read_ai_config function to return predefined config data."""
    with patch("pathlib.Path.open", new_callable=mock_open) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_read_ai_config(config_data: dict[str, str | float]) -> Generator[MagicMock, None, None]:
    """Mock the read_ai_config function to return predefined config data."""
    with patch("pathlib.Path.open", new_callable=mock_open, read_data=json.dumps(config_data)) as mock:
        yield mock


class TestConfig:
    """Tests for the Config class."""

    @pytest.fixture
    def mock_env_vars_no_rpi_ai_path(self) -> Generator[None, None, None]:
        """Mock environment variables without RPI_AI_PATH."""
        env_vars = {
            "RPI_AI_PATH": "",
            "GEMINI_API_KEY": "test_api",
        }
        with patch.dict(os.environ, env_vars):
            yield

    @pytest.fixture
    def mock_env_vars_no_gemini_api_key(self) -> Generator[None, None, None]:
        """Mock environment variables without GEMINI_API_KEY."""
        env_vars = {
            "RPI_AI_PATH": "/test/app/path",
            "GEMINI_API_KEY": "",
        }
        with patch.dict(os.environ, env_vars):
            yield

    @pytest.fixture
    def mock_path_exists(self) -> Generator[MagicMock, None, None]:
        """Mock the Path.exists method."""
        with patch("pathlib.Path.exists") as mock:
            yield mock

    def test_init(
        self,
        mock_env_vars: MagicMock,
        mock_load_config: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test initialization of the Config class."""
        config = Config()
        assert config.api_key == mock_env_vars["GEMINI_API_KEY"]
        assert config.root_dir == Path(mock_env_vars["RPI_AI_PATH"])
        mock_load_config.assert_called_once_with(config.config_file)
        mock_generate_token.assert_called_once()

    def test_init_no_rpi_ai_path(self, mock_env_vars_no_rpi_ai_path: None) -> None:
        """Test initialization when RPI_AI_PATH is not set."""
        with pytest.raises(ValueError, match="RPI_AI_PATH variable not set!"):
            Config()

    def test_init_no_api_key(self, mock_env_vars_no_gemini_api_key: None) -> None:
        """Test initialization when GEMINI_API_KEY is not set."""
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            Config()

    def test_config_dir_when_home_config_exists(
        self,
        mock_path_exists: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test config directory when home config exists."""
        mock_path_exists.return_value = True
        config = Config()
        assert config.config_dir == Path.home() / ".config" / "rpi_ai"
        assert config.config_file == config.config_dir / "ai_config.json"

    def test_config_dir_when_home_config_does_not_exist(
        self,
        mock_path_exists: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test config directory when home config does not exist."""
        mock_path_exists.return_value = False
        config = Config()
        assert config.config_dir == config.root_dir / "config"
        assert config.config_file == config.config_dir / "ai_config.json"

    def test_logs_dir(self, mock_generate_token: MagicMock) -> None:
        """Test logs directory."""
        config = Config()
        assert config.logs_dir == config.root_dir / "logs"


class TestConfigToken:
    """Tests for the token management in the Config class."""

    @pytest.fixture
    def mock_load_token_from_file(self) -> Generator[MagicMock, None, None]:
        """Mock the _load_token_from_file method in the Config class."""
        with patch("rpi_ai.config.Config._load_token_from_file") as mock:
            yield mock

    @pytest.fixture
    def mock_create_new_token(self) -> Generator[MagicMock, None, None]:
        """Mock the _create_new_token method in the Config class."""
        with patch("rpi_ai.config.Config._create_new_token") as mock:
            yield mock

    @pytest.fixture
    def mock_write_token_to_file(self) -> Generator[MagicMock, None, None]:
        """Mock the _write_token_to_file method in the Config class."""
        with patch("rpi_ai.config.Config._write_token_to_file") as mock:
            yield mock

    def test_loading_token_from_file(self, mock_pathlib_open: MagicMock, mock_load_config: MagicMock) -> None:
        """Test loading token from file."""
        mock_pathlib_open.return_value.read.return_value = "test_token"
        config = Config()
        assert config._load_token_from_file() == "test_token"

    def test_loading_token_from_file_when_file_does_not_exist(
        self,
        mock_pathlib_open: MagicMock,
        mock_generate_token: MagicMock,
        mock_load_config: MagicMock,
    ) -> None:
        """Test loading token from file when the file does not exist."""
        mock_pathlib_open.side_effect = FileNotFoundError
        config = Config()
        assert config._load_token_from_file() == ""

    def test_creating_new_token(self, mock_generate_token: MagicMock, mock_load_config: MagicMock) -> None:
        """Test creating a new token."""
        config = Config()
        assert len(config._create_new_token()) == config.TOKEN_LENGTH + 11

    def test_writing_token_to_file(
        self,
        mock_pathlib_open: MagicMock,
        mock_load_config: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test writing token to file."""
        config = Config()
        config._write_token_to_file("test_token")
        mock_pathlib_open.return_value.write.assert_called_once_with("test_token")

    def test_generating_token_loads_from_file_if_exists(
        self,
        mock_load_token_from_file: MagicMock,
        mock_load_config: MagicMock,
    ) -> None:
        """Test generating token loads from file if it exists."""
        mock_load_token_from_file.return_value = "existing_token"
        assert Config().generate_token() == "existing_token"

    def test_generating_token_writes_to_file_when_file_does_not_exist(
        self,
        mock_load_token_from_file: MagicMock,
        mock_create_new_token: MagicMock,
        mock_write_token_to_file: MagicMock,
        mock_load_config: MagicMock,
    ) -> None:
        """Test generating token writes to file when the file does not exist."""
        mock_load_token_from_file.return_value = ""
        mock_create_new_token.return_value = "new_token"
        assert Config().generate_token() == "new_token"
        mock_write_token_to_file.assert_has_calls([call("new_token")])


class TestChatbotConfig:
    """Tests for the ChatbotConfig class."""

    def test_load(self, mock_read_ai_config: MagicMock, config_data: dict[str, str | float]) -> None:
        """Test loading a ChatbotConfig from a file."""
        config = ChatbotConfig.load("dummy_path")
        mock_read_ai_config.assert_called_once()
        assert config.model == "test-model"
        assert config.max_output_tokens == config_data["max_output_tokens"]
        assert config.temperature == config_data["temperature"]

    def test_save(self, mock_read_ai_config: MagicMock, config_data: dict[str, str | float]) -> None:
        """Test saving a ChatbotConfig to a file."""
        config = ChatbotConfig.model_validate(config_data)
        config.save("dummy_path")
        mock_read_ai_config.assert_called_once_with("w")
        handle = mock_read_ai_config()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert written_data == json.dumps(config_data, indent=4)
