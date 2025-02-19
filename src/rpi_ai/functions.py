from rpi_ai.function_calling.devices.vybra_spire import VybraSpire
from rpi_ai.function_calling.system_info import SystemInfo

system_info = SystemInfo()
vybra_spire = VybraSpire()

FUNCTIONS = [
    *system_info.functions,
    *vybra_spire.functions,
]
