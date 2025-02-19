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


class AIApp:
    def __init__(self) -> None:
        self._root_dir: Path = Path()
        self._api_key: str = ""
        self._config: AIConfigType = None
        self._token: str = ""
        logger.debug("Loading environment variables...")
        load_dotenv()

        if not self.root_dir:
            msg = "RPI_AI_PATH variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        if not self.api_key:
            msg = "GEMINI_API_KEY variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.info(f"Generated token: {self.token}")

        self.chatbot = Chatbot(self.api_key, self.config, FUNCTIONS)

        self.app = Flask(__name__)
        self.app.add_url_rule("/", "is_alive", self.is_alive, methods=["GET"])
        self.app.add_url_rule("/login", "login", self.token_required(self.login), methods=["GET"])
        self.app.add_url_rule("/get-config", "get-config", self.token_required(self.get_config), methods=["GET"])
        self.app.add_url_rule(
            "/update-config", "update-config", self.token_required(self.update_config), methods=["POST"]
        )
        self.app.add_url_rule("/chat", "chat", self.token_required(self.chat), methods=["POST"])
        self.app.add_url_rule("/send-audio", "send_audio", self.token_required(self.send_audio), methods=["POST"])

    @property
    def root_dir(self) -> Path:
        if not self._root_dir:
            self._root_dir = Path(str(os.environ.get("RPI_AI_PATH")))
            logger.debug(f"Root directory: {self._root_dir}")

        return self._root_dir

    @property
    def config_dir(self) -> Path:
        return self.root_dir / "config"

    @property
    def logs_dir(self) -> Path:
        return self.root_dir / "logs"

    @property
    def api_key(self) -> str:
        if not self._api_key:
            self._api_key = str(os.environ.get("GEMINI_API_KEY"))
            logger.debug("Successfully loaded API key")

        return self._api_key

    @property
    def config(self) -> AIConfigType:
        if not self._config:
            logger.debug("Loading config...")
            self._config = AIConfigType.load(str(self.config_dir / "ai_config.json"))

        return self._config

    @property
    def token(self) -> str:
        if not self._token:
            if token := self.load_token_from_file():
                self._token = token
            else:
                self._token = self.create_new_token()
                self.write_token_to_file(self._token)

        return self._token

    def get_request_headers(self) -> Headers:
        return request.headers

    def get_request_json(self) -> dict[str, str] | None:
        return request.json

    def get_request_files(self) -> ImmutableMultiDict[str, FileStorage]:
        return request.files

    def load_token_from_file(self) -> str:
        try:
            with (self.logs_dir / "token.txt").open() as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def create_new_token(self) -> str:
        return secrets.token_urlsafe(32)

    def write_token_to_file(self, token: str) -> None:
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        with (self.logs_dir / "token.txt").open("w") as file:
            file.write(token)

    def authenticate(self) -> bool:
        return self.get_request_headers().get("Authorization") == self.token

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
        response = self.chatbot.start_chat()
        logger.info(response.message)
        return jsonify(response)

    def get_config(self) -> Response:
        return jsonify(self.chatbot.get_config())

    def update_config(self) -> Response:
        logger.info("Updating AI config...")
        config = AIConfigType(**self.get_request_json())
        self.chatbot.update_config(config)
        response = self.chatbot.start_chat()
        logger.info(response.message)
        return jsonify(response)

    def chat(self) -> Response:
        user_message = self.get_request_json()
        if user_message and user_message.get("message"):
            logger.info(user_message["message"])
            response = self.chatbot.send_message(user_message["message"])
            logger.info(response.message)
        else:
            response = "No message received."
            logger.error(response)
        return jsonify(response)

    def send_audio(self) -> Response:
        audio_file: FileStorage | None = self.get_request_files().get("audio")
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
