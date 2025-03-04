from __future__ import annotations

import os
from enum import Enum

import tinytuya

from rpi_ai.function_calling.devices.tuya_device import TuyaDevice
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class VybraSpireOptions(Enum):
    POWER = "1"
    COLD_FAN_POWER = "2"
    FAN_MODE = "3"
    HORIZONTAL_WIND = "8"
    TARGET_TEMPERATURE = "9"
    CURRENT_TEMPERATURE = "10"
    SOUND = "102"
    HEAT_MODE = "103"
    HOT_FAN_POWER = "106"
    UV_STERILISATION = "107"

    @staticmethod
    def get_valid_options() -> dict:
        return {
            "1": [False, True],  # Power
            "2": (1, 9),  # Cold fan power
            "3": ["fresh", "close", "heavy", "sleep"],  # fresh/close/strong/quiet
            "8": [False, True],  # Horizontal wind
            "9": (1, 30),  # Target temperature when heating
            "10": [],  # Current temperature
            "102": [False, True],  # Sound
            "103": [False, True],  # Cold/hot
            "106": (1, 4),  # Hot fan power
            "107": [False, True],  # UV sterilisation
        }

    @staticmethod
    def validate_option(option: VybraSpireOptions, value: int | str | bool) -> int | str | bool:
        valid_options = VybraSpireOptions.get_valid_options()

        if option.value not in valid_options:
            msg = f"Invalid option: {option}"
            raise ValueError(msg)

        if not isinstance(value, int | str | bool):
            msg = f"Invalid value type for {option}: {value}"
            raise TypeError(msg)

        valid_values = valid_options[option.value]
        if isinstance(valid_values, tuple) and isinstance(value, int):
            if valid_values[0] <= value <= valid_values[1]:
                return value
        elif isinstance(valid_values, list) and value in valid_values:
            return value

        msg = f"Invalid value for {option}: {value}"
        raise ValueError(msg)


class VybraSpire(TuyaDevice):
    try:
        DEVICE = tinytuya.Device(
            dev_id=str(os.environ.get("VYBRA_SPIRE_ID")),
            address=str(os.environ.get("VYBRA_SPIRE_ADDRESS")),
            local_key=str(os.environ.get("VYBRA_SPIRE_KEY")),
            version=os.environ.get("VYBRA_SPIRE_VERSION"),
        )
    except Exception:
        logger.exception("Failed to initialise Vybra Spire device.")

    def __init__(self) -> None:
        super().__init__()
        self.functions = [
            VybraSpire.turn_off,
            VybraSpire.turn_on,
            VybraSpire.get_current_temperature,
            VybraSpire.set_heating_mode_cold,
            VybraSpire.set_heating_mode_hot,
            VybraSpire.set_fan_mode_fresh,
            VybraSpire.set_fan_mode_close,
            VybraSpire.set_fan_mode_strong,
            VybraSpire.set_fan_mode_quiet,
            VybraSpire.turn_off_horizontal_wind,
            VybraSpire.turn_on_horizontal_wind,
            VybraSpire.turn_off_sound,
            VybraSpire.turn_on_sound,
            VybraSpire.turn_off_uv_sterilisation,
            VybraSpire.turn_on_uv_sterilisation,
        ]

    @classmethod
    def get_current_temperature(cls) -> str:
        """Get the current temperature in the room."""
        result = cls._get_value(VybraSpireOptions.CURRENT_TEMPERATURE.value)
        return f"Current temperature: {result}"

    @classmethod
    def turn_on(cls) -> str:
        """Turn on the Vybra Spire (fan/heater) device."""
        bool_value = True
        result = cls._set_value(VybraSpireOptions.POWER.value, bool_value)
        return f"Device power: {result}"

    @classmethod
    def turn_off(cls) -> str:
        """Turn off the Vybra Spire (fan/heater) device."""
        bool_value = False
        result = cls._set_value(VybraSpireOptions.POWER.value, bool_value)
        return f"Device power: {result}"

    @classmethod
    def set_heating_mode_cold(cls) -> str:
        """
        Set the heating mode to cold.
        """
        bool_value = False
        result = cls._set_value(VybraSpireOptions.HEAT_MODE.value, bool_value)
        return f"Heating mode: {result}"

    @classmethod
    def set_heating_mode_hot(cls) -> str:
        """
        Set the heating mode to hot.
        """
        bool_value = True
        result = cls._set_value(VybraSpireOptions.HEAT_MODE.value, bool_value)
        return f"Heating mode: {result}"

    @classmethod
    def set_fan_mode_fresh(cls) -> str:
        """
        Set the fan mode to fresh.
        """
        mode = "fresh"
        result = cls._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_close(cls) -> str:
        """
        Set the fan mode to close.
        """
        mode = "close"
        result = cls._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_strong(cls) -> str:
        """
        Set the fan mode to strong.
        """
        mode = "heavy"
        result = cls._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_quiet(cls) -> str:
        """
        Set the fan mode to quiet.
        """
        mode = "sleep"
        result = cls._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        return f"Fan mode: {result}"

    @classmethod
    def turn_on_horizontal_wind(cls) -> str:
        """
        Turn on the horizontal wind to rotate the device.
        """
        bool_value = True
        result = cls._set_value(VybraSpireOptions.HORIZONTAL_WIND.value, bool_value)
        return f"Horizontal wind: {result}"

    @classmethod
    def turn_off_horizontal_wind(cls) -> str:
        """
        Turn off the horizontal wind to stop rotating the device.
        """
        bool_value = False
        result = cls._set_value(VybraSpireOptions.HORIZONTAL_WIND.value, bool_value)
        return f"Horizontal wind: {result}"

    @classmethod
    def turn_on_sound(cls) -> str:
        """
        Turn on the sound.
        """
        bool_value = True
        result = cls._set_value(VybraSpireOptions.SOUND.value, bool_value)
        return f"Sound: {result}"

    @classmethod
    def turn_off_sound(cls) -> str:
        """
        Turn off the sound.
        """
        bool_value = False
        result = cls._set_value(VybraSpireOptions.SOUND.value, bool_value)
        return f"Sound: {result}"

    @classmethod
    def turn_on_uv_sterilisation(cls) -> str:
        """
        Turn on the UV sterilisation.
        """
        bool_value = True
        result = cls._set_value(VybraSpireOptions.UV_STERILISATION.value, bool_value)
        return f"UV sterilisation: {result}"

    @classmethod
    def turn_off_uv_sterilisation(cls) -> str:
        """
        Turn off the UV sterilisation.
        """
        bool_value = False
        result = cls._set_value(VybraSpireOptions.UV_STERILISATION.value, bool_value)
        return f"UV sterilisation: {result}"
