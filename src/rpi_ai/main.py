import os
import secrets
import signal
from types import FrameType

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from rpi_ai.config import AIConfigType
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class AIApp:
    def __init__(self) -> None:
        logger.debug("Loading environment variables...")
        load_dotenv()
        api_key = self.get_api_key()

        if not api_key:
            msg = "GEMINI_API_KEY variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.debug("Loading config...")
        self.config = AIConfigType.load("config/ai_config.json")

        self.chatbot = Chatbot(api_key, self.config, FUNCTIONS)

        self.token = self.generate_token()
        logger.info(f"Generated token: {self.token}")

        self.app = Flask(__name__)
        self.app.add_url_rule("/", "is_alive", self.is_alive, methods=["GET"])
        self.app.add_url_rule("/login", "login", self.token_required(self.login), methods=["GET"])
        self.app.add_url_rule("/chat", "chat", self.token_required(self.chat), methods=["POST"])
        self.app.add_url_rule("/command", "command", self.token_required(self.command), methods=["POST"])

    def get_api_key(self) -> str:
        return os.environ.get("GEMINI_API_KEY")

    def get_request_json(self) -> dict[str, str]:
        return request.json

    def get_request_headers(self) -> dict[str, str]:
        return request.headers

    def generate_token(self) -> str:
        """Generate a secure token for client authentication."""
        return secrets.token_hex(16)

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
        logger.info(response)
        return jsonify(response)

    def chat(self) -> Response:
        user_message = self.get_request_json().get("message")
        logger.info(user_message)
        response = self.chatbot.send_message(user_message)
        logger.info(response.message)
        return jsonify(response)

    def command(self) -> Response:
        user_message = self.get_request_json().get("message")
        logger.info(user_message)
        response = self.chatbot.send_command(user_message)
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
