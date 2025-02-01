import platform
import socket
from datetime import datetime

import psutil

from rpi_ai.function_calling.functions_list_base import FunctionsListBase
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class SystemInfo(FunctionsListBase):
    def __init__(self) -> None:
        super().__init__()
        self.functions = [
            SystemInfo.os_info,
            SystemInfo.hostname,
            SystemInfo.ip_address,
            SystemInfo.uptime,
            SystemInfo.get_running_processes,
            SystemInfo.cpu_percent,
            SystemInfo.memory_percent,
            SystemInfo.disk_usage,
            SystemInfo.temperature,
        ]

    @staticmethod
    def os_info() -> str:
        """
        Get the operating system information.
        """
        return str(
            {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            }
        )

    @staticmethod
    def hostname() -> str:
        """
        Get the system hostname.
        """
        return socket.gethostname()

    @staticmethod
    def ip_address() -> str:
        """
        Get the system IP address.
        """
        return socket.gethostbyname(SystemInfo.hostname())

    @staticmethod
    def uptime() -> str:
        """
        Get the system uptime.
        """
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        return str(datetime.now() - boot_time)

    @staticmethod
    def get_running_processes() -> dict:
        """
        Get the running processes.
        """
        return str({p.pid: p.info for p in psutil.process_iter(["pid", "name", "username"])})

    @staticmethod
    def cpu_percent() -> float:
        """
        Get the CPU usage percentage.
        """
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def memory_percent() -> float:
        """
        Get the memory usage percentage.
        """
        return psutil.virtual_memory().percent

    @staticmethod
    def disk_usage() -> float:
        """
        Get the disk usage percentage.
        """
        return psutil.disk_usage("/").percent

    @staticmethod
    def temperature() -> float:
        """
        Get the CPU temperature in degrees Celsius.
        `None` is returned if the temperature cannot be retrieved.
        """
        try:
            return psutil.sensors_temperatures()["cpu_thermal"][0].current
        except (KeyError, IndexError, AttributeError):
            logger.exception("Failed to get CPU temperature.")
            return None
