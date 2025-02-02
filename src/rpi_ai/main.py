import os
import secrets
import signal
from pathlib import Path
from types import FrameType

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.logger import Logger
from rpi_ai.models.types import AIConfigType

logger = Logger(__name__)


class AIApp:
    def __init__(self) -> None:
        logger.debug("Loading environment variables...")
        load_dotenv()

        if not (app_path := self.get_app_path()):
            msg = "RPI_AI_PATH variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        config_dir = Path(app_path) / "config"
        self.logs_dir = Path(app_path) / "logs"

        if not (api_key := self.get_api_key()):
            msg = "GEMINI_API_KEY variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.debug("Loading config...")
        config = AIConfigType.load(str(config_dir / "ai_config.json"))

        self.chatbot = Chatbot(api_key, config, FUNCTIONS)

        self.token = self.generate_token()
        logger.info(f"Generated token: {self.token}")

        self.app = Flask(__name__)
        self.app.add_url_rule("/", "is_alive", self.is_alive, methods=["GET"])
        self.app.add_url_rule("/login", "login", self.token_required(self.login), methods=["GET"])
        self.app.add_url_rule("/get-config", "get-config", self.token_required(self.get_config), methods=["GET"])
        self.app.add_url_rule(
            "/update-config", "update-config", self.token_required(self.update_config), methods=["POST"]
        )
        self.app.add_url_rule("/chat", "chat", self.token_required(self.chat), methods=["POST"])

    def get_app_path(self) -> str:
        return os.environ.get("RPI_AI_PATH")

    def get_api_key(self) -> str:
        return os.environ.get("GEMINI_API_KEY")

    def get_request_json(self) -> dict[str, str]:
        return request.json

    def get_request_headers(self) -> dict[str, str]:
        return request.headers

    def create_new_token(self) -> str:
        return secrets.token_urlsafe(32)

    def write_token_to_file(self, token: str) -> None:
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        with (self.logs_dir / "token.txt").open("w") as file:
            file.write(token)

    def generate_token(self) -> str:
        """Generate a secure token for client authentication."""
        token = self.create_new_token()
        self.write_token_to_file(token)
        return token

    def authenticate(self) -> bool:
        return self.get_request_headers().get("Authorization") == self.token

    def token_required(self, f: callable) -> callable:
        """Decorator to protect endpoints with token authentication."""

        def decorated_function(*args: tuple, **kwargs: dict) -> Response:
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
        user_message = self.get_request_json().get("message")
        logger.info(user_message)
        response = self.chatbot.send_message(user_message)
        logger.info(response.message)
        return jsonify(response)

    def shutdown_handler(self, signum: int, frame: FrameType) -> None:
        logger.info("Shutting down AI...")
        self.app.do_teardown_appcontext()
        os._exit(0)

    def run(self, host: str, port: int) -> None:
        signal.signal(signal.SIGINT, self.shutdown_handler)
        self.app.run(host=host, port=port)


def main() -> None:
    ai_app = AIApp()
    ai_app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
