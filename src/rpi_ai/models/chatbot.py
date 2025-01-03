import google.generativeai as genai


class Chatbot:
    def __init__(
        self, api_key: str, model: str, candidate_count: int = 1, max_output_tokens: int = 20, temperature: float = 1.0
    ) -> None:
        genai.configure(api_key=api_key)
        self._gen_config = genai.types.GenerationConfig(
            candidate_count=candidate_count,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        self._model = genai.GenerativeModel(model, generation_config=self._gen_config)
        self._chat = self._model.start_chat(
            history=[
                {"role": "user", "parts": "Hello there!"},
                {"role": "model", "parts": "Hi! How can I help you?"},
            ]
        )

    def chat(self, text: str) -> str:
        return self._chat.send_message(text).text
