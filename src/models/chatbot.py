import google.generativeai as genai


class Chatbot:
    def __init__(self, api_key: str, model: str) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    def chat(self, text: str) -> str:
        return self._model.generate_content(text).text
