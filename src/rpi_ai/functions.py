from rpi_ai.function_calling.devices.vybra_spire import VybraSpire
from rpi_ai.function_calling.system_info import SystemInfo

FUNCTIONS = [
    *SystemInfo().functions,
    *VybraSpire().functions,
]
