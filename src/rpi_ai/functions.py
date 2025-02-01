from rpi_ai.function_calling.system_info import SystemInfo
from rpi_ai.models.types import FunctionsList

system_info = SystemInfo()

FUNCTIONS = FunctionsList(
    [
        *system_info.functions,
    ]
)
