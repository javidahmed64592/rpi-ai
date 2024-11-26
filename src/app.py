import os

from dotenv import load_dotenv

from src.models.chatbot import Chatbot
from src.models.logger import Logger

if __name__ == "__main__":
    logger = Logger(__name__)
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
    response = chatbot.chat("Hello there!")
    logger.info(response)
