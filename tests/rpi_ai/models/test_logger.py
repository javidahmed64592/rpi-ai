import logging

import pytest

from rpi_ai.models.logger import Logger


@pytest.fixture
def logger() -> Logger:
    return Logger("test_logger")


class TestLogger:
    def test_debug(self, logger: Logger, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
        assert "Debug message" in caplog.text

    def test_info(self, logger: Logger, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.INFO):
            logger.info("Info message")
        assert "Info message" in caplog.text

    def test_warning(self, logger: Logger, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            logger.warning("Warning message")
        assert "Warning message" in caplog.text

    def test_error(self, logger: Logger, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.ERROR):
            logger.error("Error message")
        assert "Error message" in caplog.text

    def test_exception(self, logger: Logger, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.ERROR):
            logger.exception("Exception message")
        assert "Exception message" in caplog.text

    def test_suppress_logging(self) -> None:
        Logger.suppress_logging("test_logger")
        logger = logging.getLogger("test_logger")
        assert logger.level == logging.CRITICAL
