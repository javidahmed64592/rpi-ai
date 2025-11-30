"""RPi AI server application module."""

import json
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
    ChatbotMessage,
    ChatbotServerConfig,
    ChatbotSpeech,
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
        self.add_authenticated_route("/chat/history", self.get_chat_history, GetChatHistoryResponse, methods=["GET"])
        self.add_authenticated_route("/chat/restart", self.post_restart_chat, None, methods=["POST"])
        self.add_authenticated_route("/chat/message", self.post_message_text, PostMessageResponse, methods=["POST"])
        self.add_authenticated_route("/chat/audio", self.post_message_audio, PostAudioResponse, methods=["POST"])

    @property
    def config_dir(self) -> Path:
        """Get the configuration directory path."""
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

    async def get_chat_history(self, request: Request) -> GetChatHistoryResponse:
        """Get current chatbot conversation history."""
        logger.info("Retrieving chatbot conversation history...")
        chat_history = self.chatbot.chat_history
        logger.info("Chat history retrieved with %d messages.", len(chat_history.messages))
        return GetChatHistoryResponse(
            code=ResponseCode.OK,
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
        except json.JSONDecodeError:
            chatbot_message = ChatbotMessage.model_message(
                message="Error: Invalid JSON in request body",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.exception(chatbot_message.message)
            return PostMessageResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_message.message,
                timestamp=PostMessageResponse.current_timestamp(),
                reply=chatbot_message,
            )

        user_message = request_json.get("message", "")
        if not user_message:
            chatbot_message = ChatbotMessage.model_message(
                message="Error: No message provided in request body",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.error(chatbot_message.message)
            return PostMessageResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_message.message,
                timestamp=PostMessageResponse.current_timestamp(),
                reply=chatbot_message,
            )

        logger.info("Message: %s", user_message)
        reply = self.chatbot.send_message(user_message)
        logger.info("Reply: %s", reply.message)
        return PostMessageResponse(
            code=ResponseCode.OK,
            message="Message sent successfully",
            timestamp=PostMessageResponse.current_timestamp(),
            reply=reply,
        )

    async def post_message_audio(self, request: Request) -> PostAudioResponse:
        """Send an audio chat message."""
        try:
            logger.info("Receiving audio message...")
            form = await request.form()
        except Exception:
            chatbot_speech = ChatbotSpeech(
                bytes="",
                message="Error: Failed to parse form data",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.exception(chatbot_speech.message)
            return PostAudioResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_speech.message,
                timestamp=PostAudioResponse.current_timestamp(),
                speech_response=chatbot_speech,
            )

        if form is None:
            chatbot_speech = ChatbotSpeech(
                bytes="",
                message="Error: No form data provided in request body",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.error(chatbot_speech.message)
            return PostAudioResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_speech.message,
                timestamp=PostAudioResponse.current_timestamp(),
                speech_response=chatbot_speech,
            )

        audio_file = form.get("audio")
        if not isinstance(audio_file, bytes) and not hasattr(audio_file, "read"):
            chatbot_speech = ChatbotSpeech(
                bytes="",
                message="Error: No audio file provided in request body",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.error(chatbot_speech.message)
            return PostAudioResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_speech.message,
                timestamp=PostAudioResponse.current_timestamp(),
                speech_response=chatbot_speech,
            )

        try:
            audio_data = await audio_file.read()
        except Exception:
            chatbot_speech = ChatbotSpeech(
                bytes="",
                message="Error: Failed to read audio file",
                timestamp=self.chatbot._get_current_timestamp(),
            )
            logger.exception(chatbot_speech.message)
            return PostAudioResponse(
                code=ResponseCode.BAD_REQUEST,
                message=chatbot_speech.message,
                timestamp=PostAudioResponse.current_timestamp(),
                speech_response=chatbot_speech,
            )

        logger.info("Received audio data...")
        reply = self.chatbot.send_audio(audio_data)
        logger.info("Audio response: %s", reply.message)
        return PostAudioResponse(
            code=ResponseCode.OK,
            message="Audio processed successfully",
            timestamp=PostAudioResponse.current_timestamp(),
            speech_response=reply,
        )
