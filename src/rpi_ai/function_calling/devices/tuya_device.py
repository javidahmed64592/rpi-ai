from __future__ import annotations

import tinytuya

from rpi_ai.function_calling.functions_list_base import FunctionsListBase


class TuyaDevice(FunctionsListBase):
    DEVICE: tinytuya.Device

    @classmethod
    def _get_value(cls, index: str) -> str | bool | None:
        try:
            if status := cls.DEVICE.status():
                dps: dict = status.get("dps", {})
                return dps.get(index)
        except Exception as e:
            return f"Error when getting value: {e}"
        else:
            return "Failed to fetch device status!"

    @classmethod
    def _set_value(cls, index: str, new_val: str | bool) -> str | bool | None:
        try:
            if cls.DEVICE.status():
                cls.DEVICE.set_value(index, new_val)
                return cls._get_value(index)
        except Exception as e:
            return f"Error when setting value: {e}"
        else:
            return "Failed to fetch device status!"
