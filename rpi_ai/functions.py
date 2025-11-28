"""Function registry for the RPi AI application."""

from rpi_ai.function_calling.system_info import SystemInfo

system_info = SystemInfo()

FUNCTIONS = [
    *system_info,
]
