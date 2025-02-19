from __future__ import annotations

import os
from enum import Enum

import tinytuya

from rpi_ai.function_calling.functions_list_base import FunctionsListBase


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

        if option not in valid_options:
            msg = f"Invalid option: {option}"
            raise ValueError(msg)

        if not isinstance(value, int | str | bool):
            msg = f"Invalid value type for {option}: {value}"
            raise TypeError(msg)

        valid_values = valid_options[option]
        if isinstance(valid_values, tuple) and isinstance(value, int):
            if valid_values[0] <= value <= valid_values[1]:
                return value
        elif isinstance(valid_values, list) and value in valid_values:
            return value

        msg = f"Invalid value for {option}: {value}"
        raise ValueError(msg)


class VybraSpire(FunctionsListBase):
    DEVICE = tinytuya.Device(
        dev_id=str(os.environ.get("VYBRA_SPIRE_ID")),
        address=str(os.environ.get("VYBRA_SPIRE_ADDRESS")),
        local_key=str(os.environ.get("VYBRA_SPIRE_KEY")),
        version=float(os.environ.get("VYBRA_SPIRE_VERSION")),
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

    @staticmethod
    def _status() -> dict:
        if not (status := VybraSpire.DEVICE.status()):
            msg = "Failed to retrieve device status"
            raise RuntimeError(msg)
        return status

    @staticmethod
    def _set_value(index: str, new_val: str | bool) -> dict[str, str]:
        try:
            if VybraSpire._status():
                VybraSpire.DEVICE.set_value(index, new_val)
                return VybraSpire._status()
        except Exception as e:
            msg = f"Error when setting device value: {e}"
            raise RuntimeError(msg) from e

    @staticmethod
    def get_current_temperature() -> str:
        """Get the current temperature in the room."""
        try:
            if status := VybraSpire._status():
                dps: dict = status.get("dps")
                current_temperature = dps.get(str(VybraSpireOptions.CURRENT_TEMPERATURE.value))
                return f"Current temperature: {current_temperature}"
        except Exception as e:
            return f"Failed to get current temperature: {e}"

    @staticmethod
    def turn_on() -> str:
        """Turn on the Vybra Spire (fan/heater) device."""
        try:
            bool_value = True
            VybraSpire._set_value(VybraSpireOptions.POWER.value, bool_value)
        except Exception as e:
            return f"Failed to turn on device: {e}"
        else:
            return f"Device power: {bool_value}"

    @staticmethod
    def turn_off() -> str:
        """Turn off the Vybra Spire (fan/heater) device."""
        try:
            bool_value = False
            VybraSpire._set_value(VybraSpireOptions.POWER.value, bool_value)
        except Exception as e:
            return f"Failed to turn off device: {e}"
        else:
            return f"Device power: {bool_value}"

    @staticmethod
    def set_heating_mode_cold() -> str:
        """
        Set the heating mode to cold.
        """
        try:
            bool_value = False
            VybraSpire._set_value(VybraSpireOptions.HEAT_MODE.value, bool_value)
        except Exception as e:
            return f"Failed to set mode to cold: {e}"
        else:
            return f"Heating mode set to: {'hot' if bool_value else 'cold'}"

    @staticmethod
    def set_heating_mode_hot() -> str:
        """
        Set the heating mode to hot.
        """
        try:
            bool_value = True
            VybraSpire._set_value(VybraSpireOptions.HEAT_MODE.value, bool_value)
        except Exception as e:
            return f"Failed to set mode to hot: {e}"
        else:
            return f"Heating mode set to: {'hot' if bool_value else 'cold'}"

    @staticmethod
    def set_fan_mode_fresh() -> str:
        """
        Set the fan mode to fresh.
        """
        try:
            mode = "fresh"
            VybraSpire._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        except Exception as e:
            return f"Failed to set mode to fresh: {e}"
        else:
            return f"Fan mode set to: {mode}"

    @staticmethod
    def set_fan_mode_close() -> str:
        """
        Set the fan mode to close.
        """
        try:
            mode = "close"
            VybraSpire._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        except Exception as e:
            return f"Failed to set mode to close: {e}"
        else:
            return f"Fan mode set to: {mode}"

    @staticmethod
    def set_fan_mode_strong() -> str:
        """
        Set the fan mode to strong.
        """
        try:
            mode = "heavy"
            VybraSpire._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        except Exception as e:
            return f"Failed to set mode to strong: {e}"
        else:
            return f"Fan mode set to: {mode}"

    @staticmethod
    def set_fan_mode_quiet() -> str:
        """
        Set the fan mode to quiet.
        """
        try:
            mode = "sleep"
            VybraSpire._set_value(VybraSpireOptions.FAN_MODE.value, mode)
        except Exception as e:
            return f"Failed to set mode to quiet: {e}"
        else:
            return f"Fan mode set to: {mode}"

    @staticmethod
    def turn_on_horizontal_wind() -> str:
        """
        Turn on the horizontal wind to rotate the device.
        """
        try:
            bool_value = True
            VybraSpire._set_value(VybraSpireOptions.HORIZONTAL_WIND.value, bool_value)
        except Exception as e:
            return f"Failed to set horizontal wind: {e}"
        else:
            return f"Horizontal wind set to: {bool_value}"

    @staticmethod
    def turn_off_horizontal_wind() -> str:
        """
        Turn off the horizontal wind to stop rotating the device.
        """
        try:
            bool_value = False
            VybraSpire._set_value(VybraSpireOptions.HORIZONTAL_WIND.value, bool_value)
        except Exception as e:
            return f"Failed to set horizontal wind: {e}"
        else:
            return f"Horizontal wind set to: {bool_value}"

    @staticmethod
    def turn_on_sound() -> str:
        """
        Turn on the sound.
        """
        try:
            bool_value = True
            VybraSpire._set_value(VybraSpireOptions.SOUND.value, bool_value)
        except Exception as e:
            return f"Failed to set sound: {e}"
        else:
            return f"Sound set to: {bool_value}"

    @staticmethod
    def turn_off_sound() -> str:
        """
        Turn off the sound.
        """
        try:
            bool_value = False
            VybraSpire._set_value(VybraSpireOptions.SOUND.value, bool_value)
        except Exception as e:
            return f"Failed to set sound: {e}"
        else:
            return f"Sound set to: {bool_value}"

    @staticmethod
    def turn_on_uv_sterilisation() -> str:
        """
        Turn on the UV sterilisation.
        """
        try:
            bool_value = True
            VybraSpire._set_value(VybraSpireOptions.UV_STERILISATION.value, bool_value)
        except Exception as e:
            return f"Failed to set UV sterilisation: {e}"
        else:
            return f"UV sterilisation set to: {bool_value}"

    @staticmethod
    def turn_off_uv_sterilisation() -> str:
        """
        Turn off the UV sterilisation.
        """
        try:
            bool_value = False
            VybraSpire._set_value(VybraSpireOptions.UV_STERILISATION.value, bool_value)
        except Exception as e:
            return f"Failed to set UV sterilisation: {e}"
        else:
            return f"UV sterilisation set to: {bool_value}"
