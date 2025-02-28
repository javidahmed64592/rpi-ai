import json
import os
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, call, mock_open, patch

import pytest

from rpi_ai.config import ChatbotConfig, Config


@pytest.fixture(autouse=True)
def mock_read_ai_config(config_data: dict[str, str | float]) -> Generator[MagicMock, None, None]:
    with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(config_data)) as mock:
        yield mock


class TestConfig:
    @pytest.fixture
    def mock_env_vars_no_rpi_ai_path(self) -> Generator[None, None, None]:
        env_vars = {
            "RPI_AI_PATH": "",
            "GEMINI_API_KEY": "test_api",
        }
        with patch.dict(os.environ, env_vars):
            yield

    @pytest.fixture
    def mock_env_vars_no_gemini_api_key(self) -> Generator[None, None, None]:
        env_vars = {
            "RPI_AI_PATH": "/test/app/path",
            "GEMINI_API_KEY": "",
        }
        with patch.dict(os.environ, env_vars):
            yield

    @pytest.fixture
    def mock_path_exists(self) -> Generator[MagicMock, None, None]:
        with patch("pathlib.Path.exists") as mock:
            yield mock

    def test_init(
        self, mock_env_vars: MagicMock, mock_load_config: MagicMock, config_data: dict[str, str | float]
    ) -> None:
        config = Config()
        assert config.api_key == mock_env_vars["GEMINI_API_KEY"]
        assert config.root_dir == Path(mock_env_vars["RPI_AI_PATH"])
        mock_load_config.assert_called_once_with(str(config.config_file))

    def test_init_no_rpi_ai_path(self, mock_env_vars_no_rpi_ai_path: None) -> None:
        with pytest.raises(ValueError, match="RPI_AI_PATH variable not set!"):
            Config()

    def test_init_no_api_key(self, mock_env_vars_no_gemini_api_key: None) -> None:
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            Config()

    def test_config_dir_when_home_config_exists(self, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = True
        config = Config()
        assert config.config_dir == Path.home() / ".config" / "rpi_ai"
        assert config.config_file == config.config_dir / "ai_config.json"

    def test_config_dir_when_home_config_does_not_exist(self, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = False
        config = Config()
        assert config.config_dir == config.root_dir / "config"
        assert config.config_file == config.config_dir / "ai_config.json"

    def test_logs_dir(self) -> None:
        config = Config()
        assert config.logs_dir == config.root_dir / "logs"


class TestConfigToken:
    @pytest.fixture
    def mock_temp_logs_dir(self) -> Generator[PropertyMock, None, None]:
        with patch("rpi_ai.config.Config.logs_dir", new_callable=PropertyMock) as mock:
            yield mock

    @pytest.fixture
    def mock_load_token_from_file(self) -> Generator[MagicMock, None, None]:
        with patch("rpi_ai.config.Config._load_token_from_file") as mock:
            yield mock

    @pytest.fixture
    def mock_create_new_token(self) -> Generator[MagicMock, None, None]:
        with patch("rpi_ai.config.Config._create_new_token") as mock:
            yield mock

    @pytest.fixture
    def mock_write_token_to_file(self) -> Generator[MagicMock, None, None]:
        with patch("rpi_ai.config.Config._write_token_to_file") as mock:
            yield mock

    def test_loading_token_from_file(self, mock_temp_logs_dir: MagicMock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            token_file = temp_path / "token.txt"
            token_file.write_text("test_token")
            mock_temp_logs_dir.return_value = temp_path
            config = Config()
            assert config._load_token_from_file() == "test_token"

    def test_loading_token_from_file_when_file_does_not_exist(self, mock_temp_logs_dir: MagicMock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            mock_temp_logs_dir.return_value = temp_path
            config = Config()
            assert config._load_token_from_file() == ""

    def test_creating_new_token(self) -> None:
        config = Config()
        assert len(config._create_new_token()) == config.TOKEN_LENGTH + 11

    def test_writing_token_to_file(self, mock_temp_logs_dir: MagicMock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            token_file = temp_path / "token.txt"
            mock_temp_logs_dir.return_value = temp_path
            config = Config()
            config._write_token_to_file("test_token")
            assert token_file.read_text() == "test_token"

    def test_generating_token_loads_from_file_if_exists(
        self,
        mock_load_token_from_file: MagicMock,
    ) -> None:
        mock_load_token_from_file.return_value = "existing_token"
        assert Config().generate_token() == "existing_token"

    def test_generating_token_writes_to_file_when_file_does_not_exist(
        self,
        mock_load_token_from_file: MagicMock,
        mock_create_new_token: MagicMock,
        mock_write_token_to_file: MagicMock,
    ) -> None:
        mock_load_token_from_file.return_value = ""
        mock_create_new_token.return_value = "new_token"
        assert Config().generate_token() == "new_token"
        mock_write_token_to_file.assert_has_calls([call("new_token")])


class TestChatbotConfig:
    def test_load(self, mock_read_ai_config: MagicMock, config_data: dict[str, str | float]) -> None:
        config = ChatbotConfig.load("dummy_path")
        mock_read_ai_config.assert_called_once_with("dummy_path")
        assert config.model == "test-model"
        assert config.candidate_count == config_data["candidate_count"]
        assert config.max_output_tokens == config_data["max_output_tokens"]
        assert config.temperature == config_data["temperature"]

    def test_save(self, mock_read_ai_config: MagicMock, config_data: dict[str, str | float]) -> None:
        config = ChatbotConfig(**config_data)
        config.save("dummy_path")
        mock_read_ai_config.assert_called_once_with("dummy_path", "w")
        handle = mock_read_ai_config()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert written_data == json.dumps(config_data, indent=4)
