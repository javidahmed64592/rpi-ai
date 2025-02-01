from rpi_ai.function_calling import system_info
from rpi_ai.models.types import FunctionsList

FUNCTIONS = FunctionsList(
    [
        system_info.cpu_percent,
        system_info.memory_percent,
        system_info.disk_usage,
        system_info.temperature,
        system_info.get_running_processes,
    ]
)
