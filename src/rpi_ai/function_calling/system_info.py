import psutil


def cpu_percent() -> float:
    """
    Get the CPU usage percentage.
    """
    return psutil.cpu_percent(interval=1)


def memory_percent() -> float:
    """
    Get the memory usage percentage.
    """
    return psutil.virtual_memory().percent


def disk_usage() -> float:
    """
    Get the disk usage percentage.
    """
    return psutil.disk_usage("/").percent


def temperature() -> float:
    """
    Get the CPU temperature in degrees Celsius.
    """
    try:
        return psutil.sensors_temperatures()["cpu_thermal"][0].current
    except (KeyError, IndexError):
        return 0


def get_system_info() -> dict:
    """
    Get the system information.
    """
    return {
        "cpu": cpu_percent(),
        "memory": memory_percent(),
        "disk": disk_usage(),
        "temperature": temperature(),
    }


def get_running_processes() -> dict:
    """
    Get the running processes.
    """
    return {p.pid: p.info for p in psutil.process_iter(["pid", "name", "username"])}
