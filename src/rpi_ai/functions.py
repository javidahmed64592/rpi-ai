from rpi_ai.function_calling import system_info
from rpi_ai.models.types import FunctionsList

FUNCTIONS = FunctionsList(
    [
        system_info.os_info,
        system_info.hostname,
        system_info.ip_address,
        system_info.uptime,
        system_info.get_running_processes,
        system_info.cpu_percent,
        system_info.memory_percent,
        system_info.disk_usage,
        system_info.temperature,
    ]
)
