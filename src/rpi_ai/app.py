import os

from dotenv import load_dotenv

from rpi_ai.models.chatbot import Chatbot
from rpi_ai.models.logger import Logger


class App:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
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

        response = chatbot.chat(str(input("User: ")))
        logger.info(response)
