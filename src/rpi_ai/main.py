import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from rpi_ai.config import AIConfigType
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

        self.chatbot = Chatbot(api_key, self.config)

        self.app = Flask(__name__)
        self.app.add_url_rule("/history", "history", self.history, methods=["GET"])
        self.app.add_url_rule("/chat", "chat", self.chat, methods=["POST"])

    def get_api_key(self) -> str:
        return os.environ.get("GEMINI_API_KEY")

    def get_request_json(self) -> dict[str, str]:
        return request.json

    def history(self) -> Response:
        return jsonify(self.chatbot.chat_history)

    def chat(self) -> Response:
        user_message = self.get_request_json().get("message")
        logger.info(user_message)
        response = self.chatbot.chat(user_message)
        logger.info(response)
        return jsonify(self.chatbot.chat_history)

    def run(self, host: str, port: int) -> None:
        self.app.run(host=host, port=port)


if __name__ == "__main__":
    ai_app = AIApp()
    ai_app.run(host="0.0.0.0", port=8080)
