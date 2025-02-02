from rpi_ai.function_calling.system_info import SystemInfo
from rpi_ai.models.types import FunctionToolList

system_info = SystemInfo()

FUNCTIONS = FunctionToolList(
    [
        *system_info.functions,
    ]
)
