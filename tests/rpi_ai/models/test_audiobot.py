import base64
from io import BytesIO
from unittest.mock import MagicMock

from google.genai.types import Part

from rpi_ai.models.audiobot import get_audio_bytes_from_text, get_audio_request


def test_get_audio_request() -> None:
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
    text = "Hello, world!"
    mock_audio_fp = BytesIO()
    mock_audio_fp.write(b"test_audio_bytes")
    mock_audio_fp.seek(0)
    mock_gtts_instance = mock_gtts.return_value
    mock_gtts_instance.write_to_fp.side_effect = lambda fp: fp.write(b"test_audio_bytes")

    result = get_audio_bytes_from_text(text)
    expected_result = base64.b64encode(b"test_audio_bytes").decode("utf-8")
    assert result == expected_result
    mock_gtts.assert_called_once_with(text, lang="en", tld="co.uk")
    mock_gtts_instance.write_to_fp.assert_called_once()
