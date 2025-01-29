from rpi_ai.models.logger import Logger
from rpi_ai.models.types import FunctionsList

logger = Logger(__name__)


def start_music() -> str:
    """Play some music.

    Returns: Confirmation that music has started playing.
    """
    logger.info("Starting music!")
    return "Starting music!"


def stop_music() -> str:
    """Stop the music.

    Returns: Confirmation that music has stopped playing.
    """
    logger.info("Stopping music!")
    return "Stopping music!"


def set_lights_brightness(brightness: int) -> str:
    """Set the brightness of the room lights to the specified percentage.

    Parameters:
        brightness (int): The brightness percentage to set the lights to. This must be between 0 and 100.

    Returns:
        (str): Confirmation that the lights are on.
    """
    max_brightness = 100
    if brightness < 0 or brightness > max_brightness:
        msg = "Brightness must be between 0 and 100."
        raise ValueError(msg)
    logger.info(f"Setting brightness to {brightness}.")
    return f"Lights on at {brightness}%!"


FUNCTIONS = FunctionsList(
    [
        start_music,
        stop_music,
        set_lights_brightness,
    ]
)
