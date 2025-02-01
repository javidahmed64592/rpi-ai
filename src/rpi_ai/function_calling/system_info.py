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
    `None` is returned if the temperature cannot be retrieved.
    """
    try:
        return psutil.sensors_temperatures()["cpu_thermal"][0].current
    except (KeyError, IndexError, AttributeError):
        return None


def get_running_processes() -> dict:
    """
    Get the running processes.
    """
    return str({p.pid: p.info for p in psutil.process_iter(["pid", "name", "username"])})
