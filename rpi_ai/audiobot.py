"""Audio processing utilities for the RPi AI application."""

import base64
from collections.abc import Callable
from io import BytesIO

from google.genai.types import Part
from gtts import gTTS
from gtts.tokenizer import pre_processors


def get_audio_request(audio_data: bytes) -> list[str | Part]:
    """Create audio request with inline data.

    :param bytes audio_data:
        Audio data in bytes
    :return list[str | Part]:
        List containing message and audio part
    """
    inline_data = Part.from_bytes(
        data=audio_data,
        mime_type="audio/mp3",
    )
    return ["Respond to the voice message.", inline_data]


def get_audio_bytes_from_text(text: str) -> str:
    """Convert text to audio bytes.

    :param str text:
        Text to convert to speech
    :return str:
        Base64 encoded audio data
    """
    audio_fp = BytesIO()
    tts = gTTS(
        text,
        lang="en",
        tld="co.uk",
        pre_processor_funcs=[
            *preprocess_default_list(),
            preprocess_remove_asterisk,
            preprocess_remove_emojis,
        ],
    )
    tts.write_to_fp(audio_fp)
    return base64.b64encode(audio_fp.getvalue()).decode("utf-8")


def preprocess_default_list() -> list[Callable]:
    """Get default preprocessing functions.

    :return list[Callable]:
        List of default preprocessing functions
    """
    return [
        pre_processors.tone_marks,
        pre_processors.end_of_line,
        pre_processors.abbreviations,
        pre_processors.word_sub,
    ]


def preprocess_remove_asterisk(text: str) -> str:
    """Remove asterisk characters from text.

    :param str text:
        Input text
    :return str:
        Text with asterisks removed
    """
    return text.replace("*", "")


def preprocess_remove_emojis(text: str) -> str:
    """Remove emoji characters from text.

    :param str text:
        Input text
    :return str:
        Text with emojis removed
    """
    return text.encode("ascii", "ignore").decode("ascii")
