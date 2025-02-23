import platform
import shlex
import socket
import subprocess
from datetime import datetime

import psutil

from rpi_ai.function_calling.functions_list_base import FunctionsListBase
from rpi_ai.models.logger import Logger

logger = Logger(__name__)


class SystemInfo(FunctionsListBase):
    def __init__(self) -> None:
        super().__init__()
        self.functions = [
            SystemInfo.update_and_check_packages,
            SystemInfo.upgrade_packages,
            SystemInfo.auto_remove_packages,
            SystemInfo.reboot_system,
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
        """
        Update the list of installed packages and check for updated packages.

        `sudo apt update` and `sudo apt list --upgradable`

        Returns:
            dict: The output of the package check command.
        """
        update_commands = ["sudo", "apt", "update"]
        check_commands = ["sudo", "apt", "list", "--upgradable"]
        try:
            subprocess.run(update_commands, capture_output=True, text=True, check=True)
            result = subprocess.run(check_commands, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to update packages list: {e.stderr}")
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def upgrade_packages() -> dict:
        """
        Upgrade all packages.

        `sudo apt upgrade -y`

        Returns:
            dict: The output of the package upgrade command.
        """
        commands = ["sudo", "apt", "upgrade", "-y"]
        try:
            result = subprocess.run(commands, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to upgrade packages: {e.stderr}")
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def auto_remove_packages() -> dict:
        """
        Remove unused packages.

        `sudo apt autoremove -y`

        Returns:
            dict: The output of the package autoremove command.
        """
        commands = ["sudo", "apt", "autoremove", "-y"]
        try:
            result = subprocess.run(commands, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to remove unused packages: {e.stderr}")
            return {"stdout": e.output, "stderr": e.stderr}
        else:
            return {"stdout": result.stdout, "stderr": result.stderr}

    @staticmethod
    def reboot_system() -> str:
        """
        Reboot the system after a delay.

        `sleep 5 && sudo shutdown -r now`

        Returns:
            str: A fixed output indicating the reboot command was issued.
        """
        delay = 5
        try:
            subprocess.Popen(shlex.split(f"sleep {delay} && sudo shutdown -r now"))
        except Exception:
            logger.exception("Failed to reboot system.")
            return "Failed to reboot system."
        else:
            return f"Rebooting system in {delay} seconds..."

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
            return f"No process found with PID {pid}."

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
    def get_temperature() -> float | None:
        """
        Get the CPU temperature in degrees Celsius.

        Returns:
            float: The CPU temperature in degrees Celsius.
            `None` is returned if the temperature cannot be retrieved.
        """
        try:
            return psutil.sensors_temperatures()["cpu_thermal"][0].current
        except (KeyError, IndexError, AttributeError):
            logger.exception("Failed to get CPU temperature.")
            return None
