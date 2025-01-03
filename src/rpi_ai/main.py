import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.logger import Logger

app = Flask(__name__)
logger = Logger(__name__)


@app.route("/chat", methods=["POST"])
def chat() -> Response:
    user_message = request.json.get("message")
    response = chatbot.chat(user_message)
    logger.info(response)
    return jsonify({"response": response})


if __name__ == "__main__":
    logger.debug("Loading environment variables...")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    logger.debug("Loading config...")
    model = "gemini-1.5-flash"

    if not api_key:
        msg = "GEMINI_API_KEY variable not set!"
        logger.error(msg)
        raise ValueError(msg)

    chatbot = Chatbot(api_key, model)
    app.run(host="0.0.0.0", port=5000)
