"""Unit tests for the rpi_ai.models.audiobot module."""

import base64
from io import BytesIO
from unittest.mock import MagicMock

from google.genai.types import Part

from rpi_ai.models.audiobot import (
    get_audio_bytes_from_text,
    get_audio_request,
    preprocess_default_list,
    preprocess_remove_asterisk,
    preprocess_remove_emojis,
)


def test_get_audio_request() -> None:
    """Test the get_audio_request function."""
    audio_data = b"test_audio_data"
    expected_result = [
        "Respond to the voice message.",
        Part.from_bytes(
            data=audio_data,
            mime_type="audio/mp3",
        ),
    ]
    result = get_audio_request(audio_data)
    assert result == expected_result


def test_get_audio_bytes_from_text(mock_gtts: MagicMock) -> None:
    """Test the get_audio_bytes_from_text function."""
    text = "Hello, world!"
    mock_audio_fp = BytesIO()
    mock_audio_fp.write(b"test_audio_bytes")
    mock_audio_fp.seek(0)
    mock_gtts_instance = mock_gtts.return_value
    mock_gtts_instance.write_to_fp.side_effect = lambda fp: fp.write(b"test_audio_bytes")

    result = get_audio_bytes_from_text(text)
    expected_result = base64.b64encode(b"test_audio_bytes").decode("utf-8")
    assert result == expected_result
    mock_gtts.assert_called_once_with(
        text,
        lang="en",
        tld="co.uk",
        pre_processor_funcs=[
            *preprocess_default_list(),
            preprocess_remove_asterisk,
            preprocess_remove_emojis,
        ],
    )
    mock_gtts_instance.write_to_fp.assert_called_once()


def test_preprocess_remove_asterisk() -> None:
    """Test the preprocess_remove_asterisk function."""
    text = "Hello *world*!"
    expected_result = "Hello world!"
    result = preprocess_remove_asterisk(text)
    assert result == expected_result


def test_preprocess_remove_emojis() -> None:
    """Test the preprocess_remove_emojis function."""
    text = "Hello 🌍!"
    expected_result = "Hello !"
    result = preprocess_remove_emojis(text)
    assert result == expected_result
