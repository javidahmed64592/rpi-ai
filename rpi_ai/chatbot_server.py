"""RPi AI server application module."""

import logging
import os
from pathlib import Path

from fastapi import Request
from python_template_server.constants import CONFIG_DIR, CONFIG_FILE_NAME
from python_template_server.models import ResponseCode
from python_template_server.template_server import TemplateServer

from rpi_ai.chatbot import Chatbot
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models import (
    ChatbotConfig,
    ChatbotServerConfig,
    GetConfigResponse,
)

logger = logging.getLogger(__name__)

API_KEY_ENV_VAR = "GEMINI_API_KEY"


class ChatbotServer(TemplateServer):
    """AI chatbot server application inheriting from TemplateServer."""

    def __init__(self, config: ChatbotServerConfig | None = None) -> None:
        """Initialise the ChatbotServer by delegating to the template server.

        :param ChatbotServerConfig config: Chatbot server configuration
        """
        self.config: ChatbotServerConfig
        super().__init__(package_name="rpi-ai", config_filepath=self.config_dir / CONFIG_FILE_NAME, config=config)

        if not (gemini_api_key := os.environ.get(API_KEY_ENV_VAR)):
            msg = f"{API_KEY_ENV_VAR} variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.info("Successfully loaded API key!")
        self.chatbot = Chatbot(str(gemini_api_key), self.config.chatbot_config, FUNCTIONS)
        logger.info("Successfully initialised Chatbot!")

    def validate_config(self, config_data: dict) -> ChatbotServerConfig:
        """Validate and parse the configuration data into a ChatbotServerConfig.

        :param dict config_data: Raw configuration data
        :return ChatbotServerConfig: Validated chatbot server configuration
        """
        return ChatbotServerConfig.model_validate(config_data)  # type: ignore[no-any-return]

    def setup_routes(self) -> None:
        """Set up API routes."""
        super().setup_routes()
        self.add_authenticated_route("/config", self.get_config, GetConfigResponse, methods=["GET"])
        self.add_authenticated_route("/config", self.post_config, None, methods=["POST"])

    @property
    def config_dir(self) -> Path:
        """Get the configuration directory path.

        :return Path:
            Configuration directory path
        """
        if not (config_dir := Path.home() / ".config" / "rpi_ai").exists():
            config_dir = CONFIG_DIR

        logger.info("Config directory: %s", config_dir)
        return config_dir

    async def get_config(self, request: Request) -> GetConfigResponse:
        """Get current chatbot configuration."""
        logger.info("Retrieving chatbot configuration...")
        return GetConfigResponse(
            code=ResponseCode.OK,
            message="Successfully retrieved chatbot configuration.",
            timestamp=GetConfigResponse.current_timestamp(),
            config=self.chatbot.get_config(),
        )

    async def post_config(self, request: Request) -> None:
        """Update chatbot configuration."""
        logger.info("Updating chatbot configuration...")
        self.config.chatbot_config = ChatbotConfig.model_validate(await request.json())
        self.chatbot.update_config(self.config.chatbot_config)
        logger.info("Saving updated configuration to file: %s", self.config_filepath)
        self.config.save_to_file(self.config_filepath)
        logger.info("Restarting chatbot with updated configuration...")
        self.chatbot.start_chat()

def run() -> None:
    """Serve the FastAPI application using uvicorn.

    :raise SystemExit: If configuration fails to load or SSL certificate files are missing
    """
    server = ChatbotServer()
    server.run()


if __name__ == "__main__":
    run()
