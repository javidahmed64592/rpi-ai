from rpi_ai.function_calling.devices.vybra_spire import VybraSpire
from rpi_ai.function_calling.system_info import SystemInfo
from rpi_ai.models.logger import Logger

logger = Logger(__name__)

FUNCTIONS = SystemInfo().functions

try:
    FUNCTIONS.extend(VybraSpire().functions)
except RuntimeError:
    logger.exception("Failed to load Vybra Spire functions.")
