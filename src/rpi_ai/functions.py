from rpi_ai.models.types import FunctionsList


def start_music() -> str:
    """Play some music.

    Returns: Confirmation that music has started playing.
    """
    print("Starting music!")
    return "Starting music!"


def stop_music() -> str:
    """Stop the music.

    Returns: Confirmation that music has stopped playing.
    """
    print("Stopping music!")
    return "Stopping music!"


def turn_on_lights() -> str:
    """Turn on the lights.

    Returns: Confirmation that the lights are on.
    """
    print("Turning on the lights!")
    return "Turning on the lights!"


def turn_off_lights() -> str:
    """Turn off the lights.

    Returns: Confirmation that the lights are off.
    """
    print("Turning off the lights!")
    return "Turning off the lights!"


FUNCTIONS = FunctionsList(
    [
        start_music,
        stop_music,
        turn_on_lights,
        turn_off_lights,
    ]
)
