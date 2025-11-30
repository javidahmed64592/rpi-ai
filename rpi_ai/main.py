"""Main application module for the RPi AI FastAPI server."""

from rpi_ai.chatbot_server import ChatbotServer


def run() -> None:
    """Serve the FastAPI application using uvicorn.

    :raise SystemExit: If configuration fails to load or SSL certificate files are missing
    """
    server = ChatbotServer()
    server.run()
