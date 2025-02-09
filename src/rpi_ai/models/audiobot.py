import base64
from io import BytesIO

from gtts import gTTS


def get_request_body_from_audio(audio_data: bytes) -> dict[str, str]:
    inline_data = {
        "mime_type": "audio/ogg",
        "data": audio_data,
    }
    return {"parts": [{"inline_data": inline_data}]}


def get_audio_bytes_from_text(text: str) -> str:
    audio_fp = BytesIO()
    tts = gTTS(text, lang="en", tld="com.au")
    tts.write_to_fp(audio_fp)
    return base64.b64encode(audio_fp.getvalue()).decode("utf-8")
