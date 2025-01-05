from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_extract_parts() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.models.types.Message.extract_parts") as mock:
        yield mock
