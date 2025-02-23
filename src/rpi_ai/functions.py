from rpi_ai.function_calling.devices.vybra_spire import VybraSpire
from rpi_ai.function_calling.system_info import SystemInfo
from rpi_ai.models.logger import Logger

logger = Logger(__name__)

FUNCTIONS = SystemInfo().functions
FUNCTIONS.extend(VybraSpire().functions)
