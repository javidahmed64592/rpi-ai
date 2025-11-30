"""Main application module for the RPi AI Flask server."""

import logging
import os
import signal
from collections.abc import Callable
from datetime import datetime
from types import FrameType

from flask import Flask, Response, jsonify, request
from waitress import serve
from werkzeug.datastructures import FileStorage, Headers, ImmutableMultiDict

from rpi_ai.chatbot import Chatbot
from rpi_ai.config import ChatbotConfig, Config
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models import Message, SpeechResponse

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%d/%m/%Y | %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_request_headers() -> Headers:
    """Get request headers from current Flask request.

    :return Headers:
        Request headers
    """
    return request.headers


def get_request_json() -> dict[str, str] | None:
    """Get JSON data from current Flask request.

    :return dict[str, str] | None:
        Request JSON data or None
    """
    return request.json


def get_request_files() -> ImmutableMultiDict[str, FileStorage]:
    """Get files from current Flask request.

    :return ImmutableMultiDict[str, FileStorage]:
        Request files
    """
    return request.files


class AIApp:
    """Flask application for the RPi AI server."""

    def __init__(self) -> None:
        """Initialize the AI application with configuration and routes."""
        self.config = Config()
        self.chatbot = Chatbot(self.config.api_key, self.config.ai_config, FUNCTIONS)

        self._app = Flask(__name__)
        self._add_app_url("/", self.is_alive, ["GET"])
        self._add_app_url("/login", self.token_required(self.login), ["GET"])
        self._add_app_url("/restart-chat", self.token_required(self.restart_chat), ["POST"])
        self._add_app_url("/get-config", self.token_required(self.get_config), ["GET"])
        self._add_app_url("/update-config", self.token_required(self.update_config), ["POST"])
        self._add_app_url("/chat", self.token_required(self.chat), ["POST"])
        self._add_app_url("/send-audio", self.token_required(self.send_audio), ["POST"])

    def _add_app_url(self, endpoint: str, view_func: Callable, methods: list[str]) -> None:
        """Add URL rule to Flask application.

        :param str endpoint:
            URL endpoint
        :param Callable view_func:
            View function to handle requests
        :param list[str] methods:
            HTTP methods allowed for this endpoint
        """
        self._app.add_url_rule(endpoint, endpoint, view_func, methods=methods)

    def authenticate(self) -> bool:
        """Authenticate request using authorization header.

        :return bool:
            True if authenticated, False otherwise
        """
        return get_request_headers().get("Authorization") == self.config.token

    def token_required(self, f: Callable) -> Callable:
        """Protect endpoints with token authentication.

        :param Callable f:
            Function to protect
        :return Callable:
            Decorated function
        """

        def decorated_function(*args: tuple, **kwargs: dict) -> tuple[Response, int]:
            if not self.authenticate():
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)  # type: ignore[no-any-return]

        return decorated_function

    def is_alive(self) -> Response:
        """Health check endpoint.

        :return Response:
            JSON response indicating server status
        """
        return jsonify({"status": "alive"})

    def login(self) -> Response:
        """Login endpoint to start new chat session.

        :return Response:
            JSON response with chat history
        """
        logger.info("Starting new chat...")
        response = self.chatbot.chat_history
        logger.info("Loaded chat history: %s messages", len(response.messages))
        return jsonify(response.model_dump())

    def restart_chat(self) -> Response:
        """Restart chat session endpoint.

        :return Response:
            JSON response with new chat history
        """
        logger.info("Restarting chat...")
        self.chatbot.start_chat()
        response = self.chatbot.chat_history
        return jsonify(response.model_dump())

    def get_config(self) -> Response:
        """Get chatbot configuration endpoint.

        :return Response:
            JSON response with current configuration
        """
        return jsonify(self.chatbot.get_config().model_dump())

    def update_config(self) -> Response:
        """Update chatbot configuration endpoint.

        :return Response:
            JSON response with updated chat history
        """
        logger.info("Updating AI config...")
        config = ChatbotConfig.model_validate(get_request_json())
        self.chatbot.update_config(config)
        config.save(self.config.config_file)
        self.chatbot.start_chat()
        response = self.chatbot.chat_history
        return jsonify(response.model_dump())

    def chat(self) -> Response:
        """Chat message endpoint.

        :return Response:
            JSON response with chatbot reply
        """
        user_message = get_request_json()
        if user_message and user_message.get("message"):
            logger.info(user_message["message"])
            response = self.chatbot.send_message(user_message["message"])
            logger.info(response.message)
        else:
            response = Message.model_message(
                message="No message received.",
                timestamp=int(datetime.now().timestamp()),
            )
            logger.error(response.message)
        return jsonify(response.model_dump())

    def send_audio(self) -> Response:
        """Audio message endpoint.

        :return Response:
            JSON response with speech response
        """
        audio_file: FileStorage | None = get_request_files().get("audio")
        if audio_file:
            audio_data = audio_file.read()
            logger.info("Received audio data...")
            response = self.chatbot.send_audio(audio_data)
            logger.info(response.message)
        else:
            response = SpeechResponse(
                bytes="",
                message="No audio data received.",
                timestamp=int(datetime.now().timestamp()),
            )
            logger.error(response.message)
        return jsonify(response.model_dump())

    def shutdown_handler(self, signum: int, frame: FrameType | None) -> None:
        """Handle shutdown signal.

        :param int signum:
            Signal number
        :param FrameType | None frame:
            Current stack frame
        """
        logger.info("Shutting down AI...")
        self._app.do_teardown_appcontext()
        os._exit(0)

    def run(self, host: str, port: int) -> None:
        """Run the Flask application.

        :param str host:
            Host address to bind to
        :param int port:
            Port number to bind to
        """
        signal.signal(signal.SIGINT, self.shutdown_handler)
        serve(self._app, host=host, port=port)


def main() -> None:
    """Run the main entry point for the application."""
    ai_app = AIApp()
    ai_app.run(host="0.0.0.0", port=8080)  # noqa: S104
