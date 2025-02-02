from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flask.testing import FlaskClient

from rpi_ai.main import AIApp, main
from rpi_ai.models.types import AIConfigType

SUCCESS_CODE = 200
UNAUTHORIZED_CODE = 401


class TestAIApp:
    def test_init_no_app_path(self, mock_app_path: MagicMock) -> None:
        mock_app_path.return_value = ""
        with pytest.raises(ValueError, match="RPI_AI_PATH variable not set!"):
            AIApp()

    def test_init_no_api_key(self, mock_app_path: MagicMock, mock_api_key: MagicMock) -> None:
        mock_api_key.return_value = ""
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            AIApp()

    def test_init(self, mock_ai_app: AIApp, mock_app_path: MagicMock, mock_create_new_token: MagicMock) -> None:
        assert mock_ai_app.logs_dir == Path(f"{mock_app_path.return_value}/logs")
        assert mock_ai_app.token == mock_create_new_token.return_value

    def test_generating_token_writes_to_file(self, mock_ai_app: AIApp, mock_write_token_to_file: MagicMock) -> None:
        mock_write_token_to_file.assert_called_once_with(mock_ai_app.token)

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
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
        mock_create_new_token: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": mock_create_new_token.return_value}
        response = mock_client.get("/login")
        mock_start_chat.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_start_chat.return_value)
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
        mock_start_chat.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_start_chat.return_value)
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


def test_main(mock_ai_app_class: MagicMock) -> None:
    main()
    mock_ai_app_class.return_value.run.assert_called_once_with(host="0.0.0.0", port=8080)
