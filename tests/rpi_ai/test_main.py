from unittest.mock import MagicMock

import pytest
from flask.testing import FlaskClient

from rpi_ai.main import AIApp, main

SUCCESS_CODE = 200
UNAUTHORIZED_CODE = 401


class TestAIApp:
    def test_init_no_api_key(self, mock_api_key: MagicMock) -> None:
        mock_api_key.return_value = ""
        with pytest.raises(ValueError, match="GEMINI_API_KEY variable not set!"):
            AIApp()

    def test_authenticate_success(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
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
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
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

    def test_chat(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_send_message: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
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

    def test_command(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_send_command: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/command")
        mock_send_command.assert_called_once_with(user_message)
        mock_jsonify.assert_called_once_with(mock_send_command.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_command_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        user_message = "Hello, World!"
        mock_request_json.return_value = {"message": user_message}

        response = mock_client.post("/command")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == UNAUTHORIZED_CODE


def test_main(mock_ai_app_class: MagicMock) -> None:
    main()
    mock_ai_app_class.return_value.run.assert_called_once_with(host="0.0.0.0", port=8080)
