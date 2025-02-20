import base64
from io import BytesIO

from google.genai.types import Part
from gtts import gTTS


def get_audio_request(audio_data: bytes) -> list[str | Part]:
    inline_data = Part.from_bytes(
        data=audio_data,
        mime_type="audio/mp3",
    )
    return ["Respond to the voice message.", inline_data]


def get_audio_bytes_from_text(text: str) -> str:
    audio_fp = BytesIO()
    tts = gTTS(text, lang="en", tld="co.uk")
    tts.write_to_fp(audio_fp)
    return base64.b64encode(audio_fp.getvalue()).decode("utf-8")
