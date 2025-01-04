import google.generativeai as genai

from rpi_ai.config import AIConfigType


class Chatbot:
    def __init__(self, api_key: str, config: AIConfigType) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(config.model, generation_config=config.generation_config)
        self._chat = self._model.start_chat(
            history=[
                {"role": "user", "parts": "Hello there!"},
                {"role": "model", "parts": "Hi! How can I help you?"},
            ]
        )

    def chat(self, text: str) -> str:
        return self._chat.send_message(text).text
