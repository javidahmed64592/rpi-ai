from __future__ import annotations

import os
from enum import Enum

from rpi_ai.function_calling.devices.tuya_device import TuyaDevice


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

    def validate_option(self, value: int | str | bool) -> int | str | bool:
        valid_options = self.get_valid_options()

        if self.value not in valid_options:
            msg = f"Invalid option: {self}"
            raise ValueError(msg)

        if not isinstance(value, int | str | bool):
            msg = f"Invalid value type for {self}: {value}"
            raise TypeError(msg)

        valid_values = valid_options[self.value]
        if isinstance(valid_values, tuple) and isinstance(value, int):
            if valid_values[0] <= value <= valid_values[1]:
                return value
        elif isinstance(valid_values, list) and value in valid_values:
            return value

        msg = f"Invalid value for {self}: {value}"
        raise ValueError(msg)


class VybraSpire(TuyaDevice):
    TuyaDevice._init_device(
        dev_id=str(os.environ.get("VYBRA_SPIRE_ID")),
        address=str(os.environ.get("VYBRA_SPIRE_ADDRESS")),
        local_key=str(os.environ.get("VYBRA_SPIRE_KEY")),
        version=os.environ.get("VYBRA_SPIRE_VERSION"),
    )

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
        option = VybraSpireOptions.CURRENT_TEMPERATURE
        result = cls._get_value(option.value)
        return f"Current temperature: {result}"

    @classmethod
    def turn_on(cls) -> str:
        """Turn on the Vybra Spire (fan/heater) device."""
        option = VybraSpireOptions.POWER
        result = cls._set_value(option.value, option.validate_option(True))
        return f"Device power: {result}"

    @classmethod
    def turn_off(cls) -> str:
        """Turn off the Vybra Spire (fan/heater) device."""
        option = VybraSpireOptions.POWER
        result = cls._set_value(option.value, option.validate_option(False))
        return f"Device power: {result}"

    @classmethod
    def set_heating_mode_cold(cls) -> str:
        """
        Set the heating mode to cold.
        """
        option = VybraSpireOptions.HEAT_MODE
        result = cls._set_value(option.value, option.validate_option(False))
        return f"Heating mode: {result}"

    @classmethod
    def set_heating_mode_hot(cls) -> str:
        """
        Set the heating mode to hot.
        """
        option = VybraSpireOptions.HEAT_MODE
        result = cls._set_value(option.value, option.validate_option(True))
        return f"Heating mode: {result}"

    @classmethod
    def set_fan_mode_fresh(cls) -> str:
        """
        Set the fan mode to fresh.
        """
        option = VybraSpireOptions.FAN_MODE
        result = cls._set_value(option.value, option.validate_option("fresh"))
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_close(cls) -> str:
        """
        Set the fan mode to close.
        """
        option = VybraSpireOptions.FAN_MODE
        result = cls._set_value(option.value, option.validate_option("close"))
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_strong(cls) -> str:
        """
        Set the fan mode to strong.
        """
        option = VybraSpireOptions.FAN_MODE
        result = cls._set_value(option.value, option.validate_option("heavy"))
        return f"Fan mode: {result}"

    @classmethod
    def set_fan_mode_quiet(cls) -> str:
        """
        Set the fan mode to quiet.
        """
        option = VybraSpireOptions.FAN_MODE
        result = cls._set_value(option.value, option.validate_option("sleep"))
        return f"Fan mode: {result}"

    @classmethod
    def turn_on_horizontal_wind(cls) -> str:
        """
        Turn on the horizontal wind to rotate the device.
        """
        option = VybraSpireOptions.HORIZONTAL_WIND
        result = cls._set_value(option.value, option.validate_option(True))
        return f"Horizontal wind: {result}"

    @classmethod
    def turn_off_horizontal_wind(cls) -> str:
        """
        Turn off the horizontal wind to stop rotating the device.
        """
        option = VybraSpireOptions.HORIZONTAL_WIND
        result = cls._set_value(option.value, option.validate_option(False))
        return f"Horizontal wind: {result}"

    @classmethod
    def turn_on_sound(cls) -> str:
        """
        Turn on the sound.
        """
        option = VybraSpireOptions.SOUND
        result = cls._set_value(option.value, option.validate_option(True))
        return f"Sound: {result}"

    @classmethod
    def turn_off_sound(cls) -> str:
        """
        Turn off the sound.
        """
        option = VybraSpireOptions.SOUND
        result = cls._set_value(option.value, option.validate_option(False))
        return f"Sound: {result}"

    @classmethod
    def turn_on_uv_sterilisation(cls) -> str:
        """
        Turn on the UV sterilisation.
        """
        option = VybraSpireOptions.UV_STERILISATION
        result = cls._set_value(option.value, option.validate_option(True))
        return f"UV sterilisation: {result}"

    @classmethod
    def turn_off_uv_sterilisation(cls) -> str:
        """
        Turn off the UV sterilisation.
        """
        option = VybraSpireOptions.UV_STERILISATION
        result = cls._set_value(option.value, option.validate_option(False))
        return f"UV sterilisation: {result}"
