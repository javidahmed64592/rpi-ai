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
            SystemInfo.get_os_info,
            SystemInfo.get_hostname,
            SystemInfo.get_uptime,
            SystemInfo.get_running_processes,
            SystemInfo.get_process_name_by_pid,
            SystemInfo.get_cpu_percent,
            SystemInfo.get_memory_usage,
            SystemInfo.get_disk_usage,
            SystemInfo.temperature,
        ]

    @staticmethod
    def get_os_info() -> dict:
        """
        Get the operating system information.

        Returns:
            dict: A dictionary containing the OS information.
        """
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    @staticmethod
    def get_hostname() -> str:
        """
        Get the system hostname.

        Returns:
            str: The system hostname.
        """
        return socket.gethostname()

    @staticmethod
    def get_uptime() -> str:
        """
        Get the system uptime.

        Returns:
            str: The system uptime as a string.
        """
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        return str(datetime.now() - boot_time)

    @staticmethod
    def get_running_processes() -> dict:
        """
        Get the running processes.

        Returns:
            dict: A dictionary of running processes with PID as keys.
        """
        return {p.pid: p.info for p in psutil.process_iter(["pid", "name", "username"])}

    @staticmethod
    def get_process_name_by_pid(pid: int) -> str:
        """
        Get the name of a running process based on its PID.

        Args:
            pid (int): The process ID.

        Returns:
            str: The name of the process.
        """
        pid = int(pid)
        try:
            process = psutil.Process(pid)
            return process.name()
        except psutil.NoSuchProcess:
            logger.exception(f"No process found with PID {pid}.")

    @staticmethod
    def get_cpu_percent() -> float:
        """
        Get the CPU usage percentage.

        Returns:
            float: The CPU usage percentage.
        """
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage() -> dict:
        """
        Get the memory usage.

        Returns:
            dict: A dictionary containing memory usage information.
        """
        virtual_memory = psutil.virtual_memory()
        return {
            "total": virtual_memory.total,
            "available": virtual_memory.available,
            "used": virtual_memory.used,
            "percent": virtual_memory.percent,
        }

    @staticmethod
    def get_disk_usage() -> dict:
        """
        Get the disk usage.

        Returns:
            dict: A dictionary containing disk usage information.
        """
        disk_usage = psutil.disk_usage("/")
        return {
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent,
        }

    @staticmethod
    def _psutil_temperature() -> float:
        """
        Get the CPU temperature using `psutil`.

        Returns:
            float: The CPU temperature in degrees Celsius.
        """
        return psutil.sensors_temperatures()["cpu_thermal"][0].current

    @staticmethod
    def get_temperature() -> float:
        """
        Get the CPU temperature in degrees Celsius.

        Returns:
            float: The CPU temperature in degrees Celsius.
            `None` is returned if the temperature cannot be retrieved.
        """
        try:
            return SystemInfo._psutil_temperature()
        except (KeyError, IndexError, AttributeError):
            logger.exception("Failed to get CPU temperature.")
