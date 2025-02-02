from collections.abc import Generator
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from rpi_ai.function_calling.system_info import SystemInfo


@pytest.fixture
def mock_platform() -> Generator[MagicMock, None, None]:
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
        yield {
            "system": mock_system,
            "node": mock_node,
            "release": mock_release,
            "version": mock_version,
            "machine": mock_machine,
            "processor": mock_processor,
        }


@pytest.fixture
def mock_get_hostname() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.socket.gethostname") as mock:
        mock.return_value = "test_get_hostname"
        yield mock


@pytest.fixture
def mock_boot_time() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.boot_time") as mock:
        mock.return_value = datetime.now().timestamp() - 3600  # 1 hour ago
        yield mock


@pytest.fixture
def mock_process_iter() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.process_iter") as mock:
        mock.return_value = [Mock(info={"pid": 1234, "name": "test_process", "username": "test_user"})]
        yield mock


@pytest.fixture
def mock_process() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.Process") as mock:
        mock.return_value.name.return_value = "test_process"
        yield mock


@pytest.fixture
def mock_cpu_percent() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.cpu_percent") as mock:
        mock.return_value = 50.0
        yield mock


@pytest.fixture
def mock_virtual_memory() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.virtual_memory") as mock:
        mock.return_value.total = 100
        mock.return_value.available = 80
        mock.return_value.used = 20
        mock.return_value.percent = 20
        yield mock


@pytest.fixture
def mock_disk_usage() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.disk_usage") as mock:
        mock.return_value.total = 100
        mock.return_value.used = 80
        mock.return_value.free = 20
        mock.return_value.percent = 80
        yield mock


@pytest.fixture
def mock_psutil_temperature() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.SystemInfo._psutil_temperature") as mock:
        mock.return_value = 45.0
        yield mock


@pytest.fixture
def mock_psutil_fans() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.SystemInfo._psutil_fans") as mock:
        mock.return_value = {"fan1": 1500}
        yield mock


@pytest.fixture
def mock_psutil_battery() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.sensors_battery") as mock:
        mock.return_value.percent = 80
        mock.return_value.power_plugged = True
        mock.return_value.secsleft = 3600
        yield mock


def test_get_os_info(mock_platform: dict) -> None:
    expected_result = {
        "system": "test_system",
        "node": "test_node",
        "release": "test_release",
        "version": "test_version",
        "machine": "test_machine",
        "processor": "test_processor",
    }
    assert SystemInfo.get_os_info() == expected_result


def test_get_hostname(mock_get_hostname: MagicMock) -> None:
    assert SystemInfo.get_hostname() == "test_get_hostname"


def test_get_uptime(mock_boot_time: MagicMock) -> None:
    assert "1:00:00" in SystemInfo.get_uptime()


def test_get_running_processes(mock_process_iter: MagicMock) -> None:
    expected_result = {
        mock_process_iter.return_value[0].pid: {"pid": 1234, "name": "test_process", "username": "test_user"}
    }
    assert SystemInfo.get_running_processes() == expected_result


def test_get_process_name_by_pid(mock_process: MagicMock) -> None:
    assert SystemInfo.get_process_name_by_pid(1234) == "test_process"
    mock_process.assert_called_once_with(1234)


def test_cpu_percent(mock_cpu_percent: MagicMock) -> None:
    assert SystemInfo.get_cpu_percent() == mock_cpu_percent.return_value


def test_get_memory_usage(mock_virtual_memory: MagicMock) -> None:
    expected_result = {
        "total": mock_virtual_memory.return_value.total,
        "available": mock_virtual_memory.return_value.available,
        "used": mock_virtual_memory.return_value.used,
        "percent": mock_virtual_memory.return_value.percent,
    }
    assert SystemInfo.get_memory_usage() == expected_result


def test_get_disk_usage(mock_disk_usage: MagicMock) -> None:
    expected_result = {
        "total": mock_disk_usage.return_value.total,
        "used": mock_disk_usage.return_value.used,
        "free": mock_disk_usage.return_value.free,
        "percent": mock_disk_usage.return_value.percent,
    }
    assert SystemInfo.get_disk_usage() == expected_result


def test_get_temperature(mock_psutil_temperature: MagicMock) -> None:
    assert SystemInfo.get_temperature() == mock_psutil_temperature.return_value


def test_get_fan_speeds(mock_psutil_fans: MagicMock) -> None:
    expected_result = {"fan1": 1500}
    assert SystemInfo.get_fan_speeds() == expected_result


def test_get_battery_info(mock_psutil_battery: MagicMock) -> None:
    expected_result = {
        "percent": 80,
        "power_plugged": True,
        "secsleft": 3600,
    }
    assert SystemInfo.get_battery_info() == expected_result
