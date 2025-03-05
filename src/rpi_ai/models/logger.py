import logging


class Logger:
    def __init__(self, name: str) -> None:
        logging.basicConfig(format="%(asctime)s %(message)s", datefmt="[%d-%m-%Y|%I:%M:%S]", level=logging.DEBUG)
        self._logger = logging.getLogger(name)

    def debug(self, msg: str) -> None:
        self._logger.debug(msg.strip())

    def info(self, msg: str) -> None:
        self._logger.info(msg.strip())

    def warning(self, msg: str) -> None:
        self._logger.warning(msg.strip())

    def error(self, msg: str) -> None:
        self._logger.error(msg.strip())

    def exception(self, msg: str) -> None:
        self._logger.exception(msg.strip())

    @staticmethod
    def suppress_logging(package_name: str) -> None:
        package_logger = logging.getLogger(package_name)
        package_logger.setLevel(logging.CRITICAL)
