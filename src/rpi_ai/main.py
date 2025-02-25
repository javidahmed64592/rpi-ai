import os
import secrets
import signal
from collections.abc import Callable
from pathlib import Path
from types import FrameType

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from waitress import serve
from werkzeug.datastructures import FileStorage, Headers, ImmutableMultiDict

from rpi_ai.api_types import AIConfigType
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


def get_request_headers() -> Headers:
    return request.headers


def get_request_json() -> dict[str, str] | None:
    return request.json


def get_request_files() -> ImmutableMultiDict[str, FileStorage]:
    return request.files


class AIApp:
    def __init__(self) -> None:
        logger.debug("Loading environment variables...")
        load_dotenv()

        if not (rpi_ai_path := os.environ.get("RPI_AI_PATH")):
            msg = "RPI_AI_PATH variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        if not (gemini_api_key := os.environ.get("GEMINI_API_KEY")):
            msg = "GEMINI_API_KEY variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        self.root_dir = Path(str(rpi_ai_path.strip()))
        logger.debug(f"Root directory: {self.root_dir}")

        self.api_key = str(gemini_api_key)
        logger.debug("Successfully loaded API key!")

        self.config_path = self.config_dir / "ai_config.json"
        self.config = AIConfigType.load(str(self.config_path))
        logger.debug("Successfully loaded AI config!")
        self.chatbot = Chatbot(self.api_key, self.config, FUNCTIONS)

        self.token = self.generate_token()
        logger.info(f"Generated token: {self.token}")

        self.app = Flask(__name__)
        self.add_app_url("/", self.is_alive, ["GET"])
        self.add_app_url("/login", self.token_required(self.login), ["GET"])
        self.add_app_url("/restart-chat", self.token_required(self.restart_chat), ["POST"])
        self.add_app_url("/get-config", self.token_required(self.get_config), ["GET"])
        self.add_app_url("/update-config", self.token_required(self.update_config), ["POST"])
        self.add_app_url("/chat", self.token_required(self.chat), ["POST"])
        self.add_app_url("/send-audio", self.token_required(self.send_audio), ["POST"])

    @property
    def config_dir(self) -> Path:
        if (_config_dir := Path.home() / ".config" / "rpi_ai").exists():
            return _config_dir
        return self.root_dir / "config"

    @property
    def logs_dir(self) -> Path:
        return self.root_dir / "logs"

    def _load_token_from_file(self) -> str:
        try:
            with (self.logs_dir / "token.txt").open() as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""

    def _create_new_token(self) -> str:
        return secrets.token_urlsafe(32)

    def _write_token_to_file(self, token: str) -> None:
        token_file = self.logs_dir / "token.txt"
        with token_file.open("w") as file:
            file.write(token)

    def generate_token(self) -> str:
        if token := self._load_token_from_file():
            return token

        token = self._create_new_token()
        self._write_token_to_file(token)
        return token

    def add_app_url(self, endpoint: str, view_func: Callable, methods: list[str]) -> None:
        self.app.add_url_rule(endpoint, endpoint, view_func, methods=methods)

    def authenticate(self) -> bool:
        return get_request_headers().get("Authorization") == self.token

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
        response = self.chatbot.get_chat_history()
        logger.info(f"Loaded chat history: {len(response.messages)} messages")
        return jsonify(response)

    def restart_chat(self) -> Response:
        logger.info("Restarting chat...")
        self.chatbot.start_chat()
        response = self.chatbot.get_chat_history()
        return jsonify(response)

    def get_config(self) -> Response:
        return jsonify(self.chatbot.get_config())

    def update_config(self) -> Response:
        logger.info("Updating AI config...")
        config = AIConfigType(**get_request_json())
        self.chatbot.update_config(config)
        config.save(str(self.config_path))
        self.chatbot.start_chat()
        response = self.chatbot.get_chat_history()
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
        self.app.do_teardown_appcontext()
        os._exit(0)

    def run(self, host: str, port: int) -> None:
        signal.signal(signal.SIGINT, self.shutdown_handler)
        serve(self.app, host=host, port=port)


def main() -> None:
    ai_app = AIApp()
    ai_app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
