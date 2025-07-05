import logging
import os
import signal
from collections.abc import Callable
from types import FrameType

from flask import Flask, Response, jsonify, request
from waitress import serve
from werkzeug.datastructures import FileStorage, Headers, ImmutableMultiDict

from rpi_ai.config import ChatbotConfig, Config
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.chatbot import Chatbot

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%d/%m/%Y | %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_request_headers() -> Headers:
    return request.headers


def get_request_json() -> dict[str, str] | None:
    return request.json


def get_request_files() -> ImmutableMultiDict[str, FileStorage]:
    return request.files


class AIApp:
    def __init__(self) -> None:
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
        self._app.add_url_rule(endpoint, endpoint, view_func, methods=methods)

    def authenticate(self) -> bool:
        return get_request_headers().get("Authorization") == self.config.token

    def token_required(self, f: Callable) -> Callable:
        """Decorator to protect endpoints with token authentication."""

        def decorated_function(*args: tuple, **kwargs: dict) -> tuple[Response, int]:
            if not self.authenticate():
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)

        return decorated_function

    def is_alive(self) -> Response:
        return jsonify({"status": "alive"})

    def login(self) -> Response:
        logger.info("Starting new chat...")
        response = self.chatbot.chat_history
        logger.info(f"Loaded chat history: {len(response.messages)} messages")
        return jsonify(response)

    def restart_chat(self) -> Response:
        logger.info("Restarting chat...")
        self.chatbot.start_chat()
        response = self.chatbot.chat_history
        return jsonify(response)

    def get_config(self) -> Response:
        return jsonify(self.chatbot.get_config())

    def update_config(self) -> Response:
        logger.info("Updating AI config...")
        config = ChatbotConfig(**get_request_json())
        self.chatbot.update_config(config)
        config.save(self.config.config_file)
        self.chatbot.start_chat()
        response = self.chatbot.chat_history
        return jsonify(response)

    def chat(self) -> Response:
        user_message = get_request_json()
        if user_message and user_message.get("message"):
            logger.info(user_message["message"])
            response = self.chatbot.send_message(user_message["message"])
            logger.info(response.message)
        else:
            response = "No message received."
            logger.error(response)
        return jsonify(response)

    def send_audio(self) -> Response:
        audio_file: FileStorage | None = get_request_files().get("audio")
        if audio_file:
            audio_data = audio_file.read()
            logger.info("Received audio data...")
            response = self.chatbot.send_audio(audio_data)
            logger.info(response.message)
        else:
            response = "No audio data received."
            logger.error(response)
        return jsonify(response)

    def shutdown_handler(self, signum: int, frame: FrameType | None) -> None:
        logger.info("Shutting down AI...")
        self._app.do_teardown_appcontext()
        os._exit(0)

    def run(self, host: str, port: int) -> None:
        signal.signal(signal.SIGINT, self.shutdown_handler)
        serve(self._app, host=host, port=port)


def main() -> None:
    ai_app = AIApp()
    ai_app.run(host="0.0.0.0", port=8080)
