"""Unit tests for the rpi_ai.function_calling.system_info module."""

import subprocess
from collections.abc import Generator
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import psutil
import pytest

from rpi_ai.function_calling.system_info import SystemInfo


@pytest.fixture
def mock_subprocess_run() -> Generator[MagicMock, None, None]:
    """Mock the subprocess.run method to simulate command execution."""
    with patch("rpi_ai.function_calling.system_info.subprocess.run") as mock:
        mock.return_value.stdout = "test_output"
        yield mock


@pytest.fixture
def mock_platform() -> Generator[MagicMock, None, None]:
    """Mock the platform module to simulate system information retrieval."""
    with (
        patch("rpi_ai.function_calling.system_info.platform.system") as mock_system,
        patch("rpi_ai.function_calling.system_info.platform.node") as mock_node,
        patch("rpi_ai.function_calling.system_info.platform.release") as mock_release,
        patch("rpi_ai.function_calling.system_info.platform.version") as mock_version,
        patch("rpi_ai.function_calling.system_info.platform.machine") as mock_machine,
        patch("rpi_ai.function_calling.system_info.platform.processor") as mock_processor,
    ):
        mock_system.return_value = "test_system"
        mock_node.return_value = "test_node"
        mock_release.return_value = "test_release"
        mock_version.return_value = "test_version"
        mock_machine.return_value = "test_machine"
        mock_processor.return_value = "test_processor"
        yield MagicMock(
            system=mock_system,
            node=mock_node,
            release=mock_release,
            version=mock_version,
            machine=mock_machine,
            processor=mock_processor,
        )


@pytest.fixture
def mock_get_hostname() -> Generator[MagicMock, None, None]:
    """Mock the socket.gethostname method to return a predefined hostname."""
    with patch("rpi_ai.function_calling.system_info.socket.gethostname") as mock:
        mock.return_value = "test_get_hostname"
        yield mock


@pytest.fixture
def mock_boot_time() -> Generator[MagicMock, None, None]:
    """Mock the psutil.boot_time method to return a predefined boot time."""
    with patch("rpi_ai.function_calling.system_info.psutil.boot_time") as mock:
        mock.return_value = datetime.now().timestamp() - 3600  # 1 hour ago
        yield mock


@pytest.fixture
def mock_process_iter() -> Generator[MagicMock, None, None]:
    """Mock the psutil.process_iter method to return a list of mock processes."""
    with patch("rpi_ai.function_calling.system_info.psutil.process_iter") as mock:
        mock.return_value = [Mock(info={"pid": 1234, "name": "test_process", "username": "test_user"})]
        yield mock


@pytest.fixture
def mock_process() -> Generator[MagicMock, None, None]:
    """Mock the psutil.Process method to return a mock process."""
    with patch("rpi_ai.function_calling.system_info.psutil.Process") as mock:
        mock.return_value.name.return_value = "test_process"
        yield mock


@pytest.fixture
def mock_cpu_percent() -> Generator[MagicMock, None, None]:
    """Mock the psutil.cpu_percent method to return a predefined CPU usage percentage."""
    with patch("rpi_ai.function_calling.system_info.psutil.cpu_percent") as mock:
        mock.return_value = 50.0
        yield mock


@pytest.fixture
def mock_virtual_memory() -> Generator[MagicMock, None, None]:
    """Mock the psutil.virtual_memory method to return predefined memory usage statistics."""
    with patch("rpi_ai.function_calling.system_info.psutil.virtual_memory") as mock:
        mock.return_value.total = 100
        mock.return_value.available = 80
        mock.return_value.used = 20
        mock.return_value.percent = 20
        yield mock


@pytest.fixture
def mock_disk_usage() -> Generator[MagicMock, None, None]:
    """Mock the psutil.disk_usage method to return predefined disk usage statistics."""
    with patch("rpi_ai.function_calling.system_info.psutil.disk_usage") as mock:
        mock.return_value.total = 100
        mock.return_value.used = 80
        mock.return_value.free = 20
        mock.return_value.percent = 80
        yield mock


@pytest.fixture
def mock_psutil_temperature() -> Generator[MagicMock, None, None]:
    """Mock the psutil.sensors_temperatures method to return predefined temperature data."""
    with patch("rpi_ai.function_calling.system_info.psutil") as mock:
        mock.sensors_temperatures.return_value = {"cpu_thermal": [Mock(current=45.0)]}
        yield mock


def test_update_and_check_packages(mock_subprocess_run: MagicMock) -> None:
    """Test the update_and_check_packages method."""
    mock_subprocess_run.return_value.stderr = ""
    response = SystemInfo.update_and_check_packages()
    expected_update_commands = ["sudo", "apt", "update"]
    expected_check_commands = ["sudo", "apt", "list", "--upgradable"]
    mock_subprocess_run.assert_any_call(expected_update_commands, capture_output=True, text=True, check=True)
    mock_subprocess_run.assert_any_call(expected_check_commands, capture_output=True, text=True, check=True)
    assert response == {
        "stdout": mock_subprocess_run.return_value.stdout,
        "stderr": mock_subprocess_run.return_value.stderr,
    }


def test_update_and_check_packages_fails(mock_subprocess_run: MagicMock) -> None:
    """Test the update_and_check_packages method when it fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="test_error", output="test_output")
    response = SystemInfo.update_and_check_packages()
    assert response == {"stdout": "test_output", "stderr": "test_error"}


def test_upgrade_packages(mock_subprocess_run: MagicMock) -> None:
    """Test the upgrade_packages method."""
    mock_subprocess_run.return_value.stderr = ""
    response = SystemInfo.upgrade_packages()
    expected_commands = ["sudo", "apt", "upgrade", "-y"]
    mock_subprocess_run.assert_called_once_with(expected_commands, capture_output=True, text=True, check=True)
    assert response == {
        "stdout": mock_subprocess_run.return_value.stdout,
        "stderr": mock_subprocess_run.return_value.stderr,
    }


def test_upgrade_packages_fails(mock_subprocess_run: MagicMock) -> None:
    """Test the upgrade_packages method when it fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="test_error", output="test_output")
    response = SystemInfo.upgrade_packages()
    assert response == {"stdout": "test_output", "stderr": "test_error"}


def test_auto_remove_packages(mock_subprocess_run: MagicMock) -> None:
    """Test the auto_remove_packages method."""
    mock_subprocess_run.return_value.stderr = ""
    response = SystemInfo.auto_remove_packages()
    expected_commands = ["sudo", "apt", "autoremove", "-y"]
    mock_subprocess_run.assert_called_once_with(expected_commands, capture_output=True, text=True, check=True)
    assert response == {
        "stdout": mock_subprocess_run.return_value.stdout,
        "stderr": mock_subprocess_run.return_value.stderr,
    }


def test_auto_remove_packages_fails(mock_subprocess_run: MagicMock) -> None:
    """Test the auto_remove_packages method when it fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="test_error", output="test_output")
    response = SystemInfo.auto_remove_packages()
    assert response == {"stdout": "test_output", "stderr": "test_error"}


def test_get_os_info(mock_platform: MagicMock) -> None:
    """Test the get_os_info method."""
    os_info = SystemInfo.get_os_info()
    assert os_info["system"] == mock_platform.system.return_value
    assert os_info["node"] == mock_platform.node.return_value
    assert os_info["release"] == mock_platform.release.return_value
    assert os_info["version"] == mock_platform.version.return_value
    assert os_info["machine"] == mock_platform.machine.return_value
    assert os_info["processor"] == mock_platform.processor.return_value


def test_get_hostname(mock_get_hostname: MagicMock) -> None:
    """Test the get_hostname method."""
    assert SystemInfo.get_hostname() == mock_get_hostname.return_value


def test_get_uptime(mock_boot_time: MagicMock) -> None:
    """Test the get_uptime method."""
    assert "1:00:00" in SystemInfo.get_uptime()


def test_get_running_processes(mock_process_iter: MagicMock) -> None:
    """Test the get_running_processes method."""
    expected_result = {
        mock_process_iter.return_value[0].pid: {"pid": 1234, "name": "test_process", "username": "test_user"}
    }
    assert SystemInfo.get_running_processes() == expected_result


def test_get_process_name_by_pid(mock_process: MagicMock) -> None:
    """Test the get_process_name_by_pid method."""
    assert SystemInfo.get_process_name_by_pid(1234) == "test_process"
    mock_process.assert_called_once_with(1234)


def test_get_process_name_by_pid_returns_none_on_error(mock_process: MagicMock) -> None:
    """Test the get_process_name_by_pid method when the process does not exist."""
    mock_process.side_effect = psutil.NoSuchProcess(1234)
    assert SystemInfo.get_process_name_by_pid(1234) == "No process found with PID 1234."
    mock_process.assert_called_once_with(1234)


def test_cpu_percent(mock_cpu_percent: MagicMock) -> None:
    """Test the get_cpu_percent method."""
    assert SystemInfo.get_cpu_percent() == mock_cpu_percent.return_value


def test_get_memory_usage(mock_virtual_memory: MagicMock) -> None:
    """Test the get_memory_usage method."""
    expected_result = {
        "total": mock_virtual_memory.return_value.total,
        "available": mock_virtual_memory.return_value.available,
        "used": mock_virtual_memory.return_value.used,
        "percent": mock_virtual_memory.return_value.percent,
    }
    assert SystemInfo.get_memory_usage() == expected_result


def test_get_disk_usage(mock_disk_usage: MagicMock) -> None:
    """Test the get_disk_usage method."""
    expected_result = {
        "total": mock_disk_usage.return_value.total,
        "used": mock_disk_usage.return_value.used,
        "free": mock_disk_usage.return_value.free,
        "percent": mock_disk_usage.return_value.percent,
    }
    assert SystemInfo.get_disk_usage() == expected_result


def test_get_temperature(mock_psutil_temperature: MagicMock) -> None:
    """Test the get_temperature method."""
    assert (
        SystemInfo.get_temperature()
        == mock_psutil_temperature.sensors_temperatures.return_value["cpu_thermal"][0].current
    )


def test_get_temperature_returns_none_on_error(mock_psutil_temperature: MagicMock) -> None:
    """Test the get_temperature method when it fails to retrieve temperature data."""
    mock_psutil_temperature.sensors_temperatures.side_effect = KeyError
    assert SystemInfo.get_temperature() is None
