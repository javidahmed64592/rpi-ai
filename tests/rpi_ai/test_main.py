from unittest.mock import MagicMock

from flask.testing import FlaskClient

from rpi_ai.main import AIApp


class TestAIApp:
    def test_authenticate_success(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        assert mock_ai_app.authenticate() is True

    def test_authenticate_failure(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        assert mock_ai_app.authenticate() is False

    def test_is_alive(self, mock_client: FlaskClient, mock_jsonify: MagicMock) -> None:
        response = mock_client.get("/")
        mock_jsonify.assert_called_once_with({"status": "alive"})
        assert response.status_code == 200

    def test_login(
        self,
        mock_ai_app: AIApp,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "test_token"}
        response = mock_client.get("/login")
        mock_start_chat.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_start_chat.return_value)
        assert response.status_code == 200

    def test_login_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        response = mock_client.get("/login")
        mock_jsonify.assert_called_once_with({"error": "Unauthorized"})
        assert response.status_code == 401

    def test_chat(
        self,
        mock_ai_app: AIApp,
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
        assert response.status_code == 200

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
        assert response.status_code == 401

    def test_command(
        self,
        mock_ai_app: AIApp,
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
        assert response.status_code == 200

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
        assert response.status_code == 401
