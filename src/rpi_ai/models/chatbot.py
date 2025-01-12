import google.generativeai as genai

from rpi_ai.config import AIConfigType
from rpi_ai.models.types import Message


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(config.model, generation_config=config.generation_config)

    @property
    def first_message(self) -> dict[str, str]:
        return {"role": "model", "parts": "What's on your mind today?"}

    def start_chat(self) -> Message:
        self._chat = self._model.start_chat(history=[self.first_message])
        return Message(message=self.first_message.get("parts"))

    def send_message(self, text: str) -> Message:
        return Message(message=self._chat.send_message(text).text)
