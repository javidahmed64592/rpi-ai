"""RPi AI server application module."""

from python_template_server.template_server import TemplateServer

from rpi_ai.models import ChatbotServerConfig


class ChatbotServer(TemplateServer):
    """AI chatbot server application inheriting from TemplateServer."""

    def __init__(self, config: ChatbotServerConfig | None = None) -> None:
        """Initialize the ChatbotServer by delegating to the template server.

        :param ChatbotServerConfig config: Chatbot server configuration
        """
        super().__init__(package_name="rpi-ai", config=config)

    def validate_config(self, config_data: dict) -> ChatbotServerConfig:
        """Validate and parse the configuration data into a ChatbotServerConfig.

        :param dict config_data: Raw configuration data
        :return ChatbotServerConfig: Validated chatbot server configuration
        """
        return ChatbotServerConfig.model_validate(config_data)  # type: ignore[no-any-return]

    def setup_routes(self) -> None:
        """Set up API routes."""
        super().setup_routes()


def run() -> None:
    """Serve the FastAPI application using uvicorn.

    :raise SystemExit: If configuration fails to load or SSL certificate files are missing
    """
    server = ChatbotServer()
    server.run()


if __name__ == "__main__":
    run()
