"""Configuration management for the RPi AI application."""

from __future__ import annotations

import json
import logging
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the RPi AI application."""

    TOKEN_LENGTH = 32

    def __init__(self) -> None:
        """Initialize configuration by loading environment variables and settings."""
        logger.debug("Loading environment variables...")
        load_dotenv()

        if not (gemini_api_key := os.environ.get("GEMINI_API_KEY")):
            msg = "GEMINI_API_KEY variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        if not (rpi_ai_path := os.environ.get("RPI_AI_PATH")):
            msg = "RPI_AI_PATH variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.debug("Successfully loaded API key!")
        self.api_key = str(gemini_api_key)

        self.root_dir = Path(str(rpi_ai_path.strip()))
        logger.debug("Root directory: %s", self.root_dir)

        self.ai_config = ChatbotConfig.load(self.config_file)
        logger.debug("Successfully loaded AI config!")

        self.token = self.generate_token()
        logger.info("Token: %s", self.token)

    @property
    def config_dir(self) -> Path:
        """Get the configuration directory path.

        :return Path:
            Configuration directory path
        """
        if not (config_dir := Path.home() / ".config" / "rpi_ai").exists():
            config_dir = self.root_dir / "config"

        logger.debug("Config directory: %s", config_dir)
        return config_dir

    @property
    def config_file(self) -> Path:
        """Get the configuration file path.

        :return Path:
            Configuration file path
        """
        config_file = self.config_dir / "ai_config.json"
        logger.debug("Config file: %s", config_file)
        return config_file

    @property
    def logs_dir(self) -> Path:
        """Get the logs directory path.

        :return Path:
            Logs directory path
        """
        return self.root_dir / "logs"

    def _load_token_from_file(self) -> str:
        """Load authentication token from file.

        :return str:
            Token string or empty string if not found
        """
        try:
            with (self.logs_dir / "token.txt").open() as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""

    def _create_new_token(self) -> str:
        """Create a new authentication token.

        :return str:
            New token string
        """
        return secrets.token_urlsafe(self.TOKEN_LENGTH)

    def _write_token_to_file(self, token: str) -> None:
        """Write authentication token to file.

        :param str token:
            Token to write to file
        """
        token_file = self.logs_dir / "token.txt"
        with token_file.open("w") as file:
            file.write(token)

    def generate_token(self) -> str:
        """Generate or load authentication token.

        :return str:
            Authentication token
        """
        if token := self._load_token_from_file():
            return token

        token = self._create_new_token()
        self._write_token_to_file(token)
        return token


class ChatbotConfig(BaseModel):
    """Configuration for chatbot settings."""

    model: str
    system_instruction: str
    max_output_tokens: int = 20
    temperature: float = 1.0

    @classmethod
    def load(cls, path: Path) -> ChatbotConfig:
        """Load chatbot configuration from JSON file.

        :param Path path:
            Path to configuration file
        :return ChatbotConfig:
            Loaded configuration
        """
        with path.open() as file:
            return cls(**json.load(file))

    def save(self, path: Path) -> None:
        """Save chatbot configuration to JSON file.

        :param Path path:
            Path to save configuration
        """
        with path.open("w") as file:
            json.dump(self.__dict__, file, indent=4)
