from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class Config:
    def __init__(self) -> None:
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
        logger.debug(f"Root directory: {self.root_dir}")

        self.ai_config = ChatbotConfig.load(str(self.config_file))
        logger.debug("Successfully loaded AI config!")

    @property
    def config_dir(self) -> Path:
        if not (config_dir := Path.home() / ".config" / "rpi_ai").exists():
            config_dir = self.root_dir / "config"

        logger.debug(f"Config directory: {config_dir}")
        return config_dir

    @property
    def config_file(self) -> Path:
        config_file = self.config_dir / "ai_config.json"
        logger.debug(f"Config file: {config_file}")
        return config_file

    @property
    def logs_dir(self) -> Path:
        return self.root_dir / "logs"


@dataclass
class ChatbotConfig:
    model: str
    system_instruction: str
    candidate_count: int = 1
    max_output_tokens: int = 20
    temperature: float = 1.0

    @classmethod
    def load(cls, path: Path) -> ChatbotConfig:
        with open(str(path)) as file:
            return cls(**json.load(file))

    def save(self, path: str) -> None:
        with open(path, "w") as file:
            json.dump(self.__dict__, file, indent=4)
