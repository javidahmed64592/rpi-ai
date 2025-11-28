"""System information functions for the RPi AI application."""

import logging
import platform
import socket
import subprocess
from datetime import datetime

import psutil

from rpi_ai.function_calling.functions_list_base import FunctionsListBase

logger = logging.getLogger(__name__)


class SystemInfo(FunctionsListBase):
    """System information functions for monitoring system state."""

    def setup_functions(self) -> None:
        """Set up system information functions."""
        self.functions = [
            SystemInfo.update_and_check_packages,
            SystemInfo.upgrade_packages,
            SystemInfo.auto_remove_packages,
            SystemInfo.get_os_info,
            SystemInfo.get_hostname,
            SystemInfo.get_uptime,
            SystemInfo.get_running_processes,
            SystemInfo.get_process_name_by_pid,
            SystemInfo.get_cpu_percent,
            SystemInfo.get_memory_usage,
            SystemInfo.get_disk_usage,
            SystemInfo.get_temperature,
        ]

    @staticmethod
    def update_and_check_packages() -> dict:
        """Update the list of installed packages and check for updated packages.

        `sudo apt update` and `sudo apt list --upgradable`

        :return dict:
            The output of the package check command
        """
        try:
            subprocess.run(["/usr/bin/sudo", "/usr/bin/apt", "update"], capture_output=True, text=True, check=True)
            result = subprocess.run(
                ["/usr/bin/sudo", "/usr/bin/apt", "list", "--upgradable"], capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            logger.exception("Failed to update packages list: %s", e.stderr)
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def upgrade_packages() -> dict:
        """Upgrade all packages.

        `sudo apt upgrade -y`

        :return dict:
            The output of the package upgrade command
        """
        try:
            result = subprocess.run(
                ["/usr/bin/sudo", "/usr/bin/apt", "upgrade", "-y"], capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            logger.exception("Failed to upgrade packages: %s", e.stderr)
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def auto_remove_packages() -> dict:
        """Remove unused packages.

        `sudo apt autoremove -y`

        :return dict:
            The output of the package autoremove command
        """
        try:
            result = subprocess.run(
                ["/usr/bin/sudo", "/usr/bin/apt", "autoremove", "-y"], capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            logger.exception("Failed to remove unused packages: %s", e.stderr)
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def get_os_info() -> dict:
        """Get the operating system information.

        :return dict:
            A dictionary containing the OS information
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
        """Get the system hostname.

        :return str:
            The system hostname
        """
        return socket.gethostname()

    @staticmethod
    def get_uptime() -> str:
        """Get the system uptime.

        :return str:
            The system uptime as a string
        """
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        return str(datetime.now() - boot_time)

    @staticmethod
    def get_running_processes() -> dict:
        """Get the running processes.

        :return dict:
            A dictionary of running processes with PID as keys
        """
        return {p.pid: p.info for p in psutil.process_iter(["pid", "name", "username"])}

    @staticmethod
    def get_process_name_by_pid(pid: int) -> str:
        """Get the name of a running process based on its PID.

        :param int pid:
            The process ID
        :return str:
            The name of the process
        """
        pid = int(pid)
        try:
            return str(psutil.Process(pid).name())
        except psutil.NoSuchProcess:
            msg = f"No process found with PID {pid}."
            logger.exception(msg)
            return msg

    @staticmethod
    def get_cpu_percent() -> float:
        """Get the CPU usage percentage.

        :return float:
            The CPU usage percentage
        """
        return float(psutil.cpu_percent(interval=1))

    @staticmethod
    def get_memory_usage() -> dict:
        """Get the memory usage.

        :return dict:
            A dictionary containing memory usage information
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
        """Get the disk usage.

        :return dict:
            A dictionary containing disk usage information
        """
        disk_usage = psutil.disk_usage("/")
        return {
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent,
        }

    @staticmethod
    def get_temperature() -> float | None:
        """Get the CPU temperature in degrees Celsius.

        :return float | None:
            The CPU temperature in degrees Celsius or None if unavailable
        """
        try:
            return float(psutil.sensors_temperatures()["cpu_thermal"][0].current)
        except (TypeError, KeyError, IndexError, AttributeError):
            logger.exception("Failed to get CPU temperature.")
            return None
