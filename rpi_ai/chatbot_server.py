"""RPi AI server application module."""

import json
import logging
import os

from fastapi import HTTPException, Request
from pydantic import ValidationError
from python_template_server.constants import CONFIG_DIR
from python_template_server.models import ResponseCode
from python_template_server.template_server import TemplateServer

from rpi_ai.chatbot import Chatbot
from rpi_ai.functions import FUNCTIONS
from rpi_ai.models import (
    ChatbotConfig,
    ChatbotServerConfig,
    GetChatHistoryResponse,
    GetConfigResponse,
    PostAudioResponse,
    PostMessageResponse,
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
        super().__init__(package_name="rpi-ai", config=config)

        if not (gemini_api_key := os.environ.get(API_KEY_ENV_VAR)):
            msg = f"{API_KEY_ENV_VAR} variable not set!"
            logger.error(msg)
            raise ValueError(msg)

        logger.info("Successfully loaded API key!")
        self.chatbot = Chatbot(
            api_key=str(gemini_api_key),
            config_dir=CONFIG_DIR,
            config=self.config.chatbot_config,
            embedding_config=self.config.embedding_config,
            functions=FUNCTIONS,
        )
        logger.info("Successfully initialised Chatbot!")

    def validate_config(self, config_data: dict) -> ChatbotServerConfig:
        """Validate and parse the configuration data into a ChatbotServerConfig.

        :param dict config_data: Raw configuration data
        :return ChatbotServerConfig: Validated chatbot server configuration
        """
        try:
            return ChatbotServerConfig.model_validate(config_data)  # type: ignore[no-any-return]
        except ValidationError:
            logger.warning("Invalid configuration data, loading default configuration.")
            return ChatbotServerConfig.model_validate({})  # type: ignore[no-any-return]

    def setup_routes(self) -> None:
        """Set up API routes."""
        self.add_authenticated_route(
            endpoint="/config",
            handler_function=self.get_config,
            response_model=GetConfigResponse,
            methods=["GET"],
            limited=True,
        )
        self.add_authenticated_route(
            endpoint="/config",
            handler_function=self.post_config,
            response_model=None,
            methods=["POST"],
            limited=True,
        )
        self.add_authenticated_route(
            endpoint="/chat/history",
            handler_function=self.get_chat_history,
            response_model=GetChatHistoryResponse,
            methods=["GET"],
            limited=True,
        )
        self.add_authenticated_route(
            endpoint="/chat/restart",
            handler_function=self.post_restart_chat,
            response_model=None,
            methods=["POST"],
            limited=True,
        )
        self.add_authenticated_route(
            endpoint="/chat/message",
            handler_function=self.post_message_text,
            response_model=PostMessageResponse,
            methods=["POST"],
            limited=True,
        )
        self.add_authenticated_route(
            endpoint="/chat/audio",
            handler_function=self.post_message_audio,
            response_model=PostAudioResponse,
            methods=["POST"],
            limited=True,
        )

    async def get_config(self, request: Request) -> GetConfigResponse:
        """Get current chatbot configuration."""
        logger.info("Retrieving chatbot configuration...")
        return GetConfigResponse(
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

    async def get_chat_history(self, request: Request) -> GetChatHistoryResponse:
        """Get current chatbot conversation history."""
        logger.info("Retrieving chatbot conversation history...")
        chat_history = self.chatbot.chat_history
        logger.info("Chat history retrieved with %d messages.", len(chat_history.messages))
        return GetChatHistoryResponse(
            message="Successfully retrieved chatbot conversation history.",
            timestamp=GetChatHistoryResponse.current_timestamp(),
            chat_history=chat_history,
        )

    async def post_restart_chat(self, request: Request) -> None:
        """Restart chat session."""
        logger.info("Restarting chatbot session...")
        self.chatbot.start_chat()

    async def post_message_text(self, request: Request) -> PostMessageResponse:
        """Send a text chat message."""
        try:
            logger.info("Receiving user message...")
            request_json = await request.json()
        except json.JSONDecodeError as e:
            error_msg = "Invalid JSON in request body"
            logger.exception(error_msg)
            raise HTTPException(status_code=ResponseCode.BAD_REQUEST, detail=error_msg) from e

        user_message = request_json.get("message", "")
        if not user_message:
            error_msg = "No message provided in request body"
            logger.error(error_msg)
            raise HTTPException(status_code=ResponseCode.BAD_REQUEST, detail=error_msg)

        logger.info("Message: %s", user_message)
        reply = self.chatbot.send_message(user_message)
        logger.info("Reply: %s", reply.message)
        return PostMessageResponse(
            message="Message sent successfully",
            timestamp=PostMessageResponse.current_timestamp(),
            reply=reply,
        )

    async def post_message_audio(self, request: Request) -> PostAudioResponse:
        """Send an audio chat message."""
        try:
            logger.info("Receiving audio message...")
            form = await request.form()
        except Exception as e:
            error_msg = "Failed to parse form data"
            logger.exception(error_msg)
            raise HTTPException(status_code=ResponseCode.BAD_REQUEST, detail=error_msg) from e

        audio_file = form.get("audio")
        if not isinstance(audio_file, bytes) and not hasattr(audio_file, "read"):
            error_msg = "No audio file provided in request body"
            logger.error(error_msg)
            raise HTTPException(status_code=ResponseCode.BAD_REQUEST, detail=error_msg)

        try:
            audio_data = await audio_file.read()  # type: ignore[union-attr]
        except Exception as e:
            error_msg = "Failed to read audio file"
            logger.exception(error_msg)
            raise HTTPException(status_code=ResponseCode.BAD_REQUEST, detail=error_msg) from e

        logger.info("Received audio data...")
        reply = self.chatbot.send_audio(audio_data)
        logger.info("Audio response: %s", reply.message)
        return PostAudioResponse(
            message="Audio processed successfully",
            timestamp=PostAudioResponse.current_timestamp(),
            reply=reply,
        )
