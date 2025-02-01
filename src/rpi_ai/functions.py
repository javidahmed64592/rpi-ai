from rpi_ai.function_calling import system_info
from rpi_ai.models.types import FunctionsList

FUNCTIONS = FunctionsList(
    [
        system_info.get_system_info,
        system_info.get_running_processes,
    ]
)
