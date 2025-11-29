"""Unit tests for the rpi_ai.main module."""

from unittest.mock import MagicMock

from flask.testing import FlaskClient

from rpi_ai.api_types import Message, SpeechResponse
from rpi_ai.config import ChatbotConfig
from rpi_ai.main import AIApp, main

SUCCESS_CODE = 200
UNAUTHORIZED_CODE = 401

TEST_HOST = "0.0.0.0"  # noqa: S104
TEST_PORT = 8080


class TestAIApp:
    """Tests for the AIApp class in the rpi_ai.main module."""

    def test_authenticate_success(
        self, mock_ai_app: AIApp, mock_request_headers: MagicMock, mock_generate_token: MagicMock
    ) -> None:
        """Test successful authentication."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        assert mock_ai_app.authenticate() is True

    def test_authenticate_failure(self, mock_ai_app: AIApp, mock_request_headers: MagicMock) -> None:
        """Test failed authentication."""
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        assert mock_ai_app.authenticate() is False

    def test_is_alive(self, mock_client: FlaskClient, mock_jsonify: MagicMock) -> None:
        """Test the is_alive endpoint."""
        response = mock_client.get("/")
        mock_jsonify.assert_called_once_with({"status": "alive"})
        assert response.status_code == SUCCESS_CODE

    def test_login(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_chat_history: MagicMock,
        mock_jsonify: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the login endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        response = mock_client.get("/login")
        mock_chat_history.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_login_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        """Test the login endpoint with unauthorized access."""
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
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the get_config endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        response = mock_client.get("/get-config")
        mock_jsonify.assert_called_once_with(mock_get_config.return_value.model_dump())
        assert response.status_code == SUCCESS_CODE

    def test_get_config_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        """Test the get_config endpoint with unauthorized access."""
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
        mock_chat_history: MagicMock,
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the update_config endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        new_config = {
            "model": "new-model",
            "system_instruction": "new-instruction",
            "max_output_tokens": 100,
            "temperature": 0.9,
        }
        mock_request_json.return_value = new_config

        response = mock_client.post("/update-config")
        mock_update_config.assert_called_once_with(ChatbotConfig.model_validate(new_config))
        mock_save_config.assert_called_once()
        mock_start_chat.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_update_config_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_json: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        """Test the update_config endpoint with unauthorized access."""
        mock_request_headers.return_value = {"Authorization": "wrong_token"}
        new_config = {
            "model": "new-model",
            "system_instruction": "new-instruction",
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
        mock_chat_history: MagicMock,
        mock_start_chat: MagicMock,
        mock_jsonify: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the restart-chat endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        response = mock_client.post("/restart-chat")
        mock_start_chat.assert_called_once()
        mock_jsonify.assert_called_once_with(mock_chat_history.return_value)
        assert response.status_code == SUCCESS_CODE

    def test_restart_chat_unauthorized(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_jsonify: MagicMock,
    ) -> None:
        """Test the restart-chat endpoint with unauthorized access."""
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
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the chat endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
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
        """Test the chat endpoint with unauthorized access."""
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
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the chat endpoint when no message is provided."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        mock_request_json.return_value = {}

        response = mock_client.post("/chat")
        mock_send_message.assert_not_called()
        call_args = mock_jsonify.call_args
        assert call_args is not None
        arg = call_args[0][0]
        assert isinstance(arg, Message)
        assert arg.message == "No message received."
        assert arg.is_user_message is False
        assert isinstance(arg.timestamp, int)
        assert response.status_code == SUCCESS_CODE

    def test_send_audio(
        self,
        mock_client: FlaskClient,
        mock_request_headers: MagicMock,
        mock_request_files: MagicMock,
        mock_send_audio: MagicMock,
        mock_jsonify: MagicMock,
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the send-audio endpoint."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
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
        """Test the send-audio endpoint with unauthorized access."""
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
        mock_generate_token: MagicMock,
    ) -> None:
        """Test the send-audio endpoint when no audio data is provided."""
        mock_request_headers.return_value = {"Authorization": mock_generate_token.return_value}
        mock_request_files.return_value = {}

        response = mock_client.post("/send-audio")
        mock_send_audio.assert_not_called()
        call_args = mock_jsonify.call_args
        assert call_args is not None
        arg = call_args[0][0]
        assert isinstance(arg, SpeechResponse)
        assert arg.message == "No audio data received."
        assert arg.bytes == ""
        assert isinstance(arg.timestamp, int)
        assert response.status_code == SUCCESS_CODE

    def test_run_with_waitress(self, mock_ai_app: AIApp, mock_waitress_serve: MagicMock) -> None:
        """Test running the AIApp with Waitress."""
        mock_ai_app.run(host=TEST_HOST, port=TEST_PORT)
        mock_waitress_serve.assert_called_once_with(mock_ai_app._app, host=TEST_HOST, port=TEST_PORT)


def test_main(mock_ai_app_class: MagicMock) -> None:
    """Test the main function to ensure it runs the AIApp."""
    main()
    mock_ai_app_class.return_value.run.assert_called_once_with(host=TEST_HOST, port=TEST_PORT)
