import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from flask.testing import FlaskClient

from rpi_ai.api_types import AIConfigType
from rpi_ai.main import AIApp, main

SUCCESS_CODE = 200
UNAUTHORIZED_CODE = 401


@pytest.fixture
def mock_env_vars_no_rpi_ai_path() -> Generator[None, None, None]:
    env_vars = {
        "RPI_AI_PATH": "",
        "GEMINI_API_KEY": "test_api",
    }
    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def mock_env_vars_no_gemini_api_key() -> Generator[None, None, None]:
    env_vars = {
        "RPI_AI_PATH": "/test/app/path",
        "GEMINI_API_KEY": "",
    }
    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def mock_path_exists() -> Generator[MagicMock, None, None]:
    with patch("pathlib.Path.exists") as mock:
        yield mock


class TestAIAppInit:
    def test_init(self, mock_ai_app: AIApp, mock_env_vars: MagicMock) -> None:
        assert mock_ai_app.root_dir == Path(mock_env_vars["RPI_AI_PATH"])
        assert mock_ai_app.api_key == mock_env_vars["GEMINI_API_KEY"]

    def test_init_no_rpi_ai_path(self, mock_env_vars_no_rpi_ai_path: None) -> None:
        with pytest.raises(ValueError, match="RPI_AI_PATH variable not set!"):
            AIApp()

    def test_init_no_api_key(self, mock_env_vars_no_gemini_api_key: None) -> None:
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            AIApp()

    def test_config_dir_when_home_config_exists(self, mock_ai_app: AIApp, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = True
        assert mock_ai_app.config_dir == Path.home() / ".config" / "rpi_ai"

    def test_config_dir_when_home_config_does_not_exist(self, mock_ai_app: AIApp, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = False
        assert mock_ai_app.config_dir == mock_ai_app.root_dir / "config"

    def test_logs_dir(self, mock_ai_app: AIApp) -> None:
        assert mock_ai_app.logs_dir == mock_ai_app.root_dir / "logs"


class TestAIAppToken:
    def test_generating_token_loads_from_file_if_exists(
        self,
        mock_ai_app: AIApp,
        mock_load_token_from_file: MagicMock,
    ) -> None:
        mock_load_token_from_file.return_value = "existing_token"
        assert mock_ai_app.generate_token() == "existing_token"

    def test_generating_token_writes_to_file_when_file_does_not_exist(
        self,
        mock_ai_app: AIApp,
        mock_load_token_from_file: MagicMock,
        mock_create_new_token: MagicMock,
        mock_write_token_to_file: MagicMock,
    ) -> None:
        mock_load_token_from_file.return_value = ""
        mock_create_new_token.return_value = "new_token"
        assert mock_ai_app.generate_token() == "new_token"
        mock_write_token_to_file.assert_has_calls([call("new_token")])


class TestAIAppEndpoints:
    def test_authenticate_success(
        self, mock_ai_app: AIApp, mock_request_headers: MagicMock, mock_create_new_token: MagicMock
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        assert mock_ai_app.authenticate() is True

    def test_authenticate_failure(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        assert mock_ai_app.authenticate() is False

    def test_is_alive(self, mock_client: FlaskClient, mock_jsonify: MagicMock) -> None:
        response = mock_client.get("/")
        mock_jsonify.assert_called_once_with({"status": "alive"})
        assert response.status_code == SUCCESS_CODE

    def test_login(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_get_chat_history: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        response = mock_client.get("/login")
        mock_get_chat_history.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_get_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_login_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        response = mock_client.get("/login")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_get_config(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_get_config: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        response = mock_client.get("/get-config")
        mock_jsonify.assert_called_once_with(mock_get_config.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_get_config_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        response = mock_client.get("/get-config")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_update_config(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_update_config: MagicMock,
        mock_save_config: MagicMock,
        mock_get_chat_history: MagicMock,
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        new_config = {
            "model": "new-model",
            "system_instruction": "new-instruction",
            "candidate_count": 3,
            "max_output_tokens": 100,
            "temperature": 0.9,
        }
        mock_request_json.return_value = new_config

        response = mock_client.post("/update-config")
        mock_update_config.assert_called_once_with(AIConfigType(**new_config))
        mock_save_config.assert_called_once()
        mock_start_chat.assert_called_once()
        mock_get_chat_history.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_get_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_update_config_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        new_config = {
            "model": "new-model",
            "system_instruction": "new-instruction",
            "candidate_count": 3,
            "max_output_tokens": 100,
            "temperature": 0.9,
        }
        mock_request_json.return_value = new_config

        response = mock_client.post("/update-config")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_restart_chat(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_get_chat_history: MagicMock,
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        response = mock_client.post("/restart-chat")
        mock_start_chat.assert_called_once()
        mock_get_chat_history.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_get_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_restart_chat_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        response = mock_client.post("/restart-chat")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_chat(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_send_message: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/chat")
        mock_send_message.assert_called_once_with(user_message)
        mock_jsonify.assert_called_once_with(mock_send_message.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_chat_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/chat")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_chat_no_message(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_send_message: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        mock_request_json.return_value = {}

        response = mock_client.post("/chat")
        mock_send_message.assert_not_called()
        mock_jsonify.assert_called_once_with("No message received.")
        assert response.status_code == SUCCESS_CODE

    def test_send_audio(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_files: MagicMock,
        mock_send_audio: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        mock_request_files.return_value = {"audio": MagicMock(read=MagicMock(return_value="audio_data"))}

        response = mock_client.post("/send-audio")
        mock_send_audio.assert_called_once_with("audio_data")
        mock_jsonify.assert_called_once_with(mock_send_audio.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_send_audio_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_files: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        mock_request_files.return_value = {"audio": MagicMock(read=MagicMock(return_value="audio_data"))}

        response = mock_client.post("/send-audio")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE

    def test_send_audio_no_audio(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_files: MagicMock,
        mock_send_audio: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        mock_request_files.return_value = {}

        response = mock_client.post("/send-audio")
        mock_send_audio.assert_not_called()
        mock_jsonify.assert_called_once_with("No audio data received.")
        assert response.status_code == SUCCESS_CODE

    def test_run_with_waitress(self, mock_ai_app: AIApp, mock_waitress_serve: MagicMock) -> None:
        mock_ai_app.run(host="0.0.0.0", port=8080)
        mock_waitress_serve.assert_called_once_with(mock_ai_app.app, host="0.0.0.0", port=8080)


def test_main(mock_ai_app_class: MagicMock) -> None:
    main()
    mock_ai_app_class.return_value.run.assert_called_once_with(host="0.0.0.0", port=8080)
