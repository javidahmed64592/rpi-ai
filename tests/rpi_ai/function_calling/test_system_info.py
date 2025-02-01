from collections.abc import Generator
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from rpi_ai.function_calling.system_info import (
    cpu_percent,
    disk_usage,
    get_running_processes,
    hostname,
    ip_address,
    memory_percent,
    os_info,
    temperature,
    uptime,
)


@pytest.fixture
def mock_cpu_percent() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.cpu_percent") as mock:
        mock.return_value = 50.0
        yield mock


@pytest.fixture
def mock_virtual_memory() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.virtual_memory") as mock:
        mock.return_value.percent = 75.0
        yield mock


@pytest.fixture
def mock_disk_usage() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.disk_usage") as mock:
        mock.return_value.percent = 60.0
        yield mock


@pytest.fixture
def mock_sensors_temperatures() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.sensors_temperatures") as mock:
        mock.return_value = {"cpu_thermal": [Mock(current=45.0)]}
        yield mock


@pytest.fixture
def mock_process_iter() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.process_iter") as mock:
        mock.return_value = [Mock(info={"pid": 1234, "name": "test_process", "username": "test_user"})]
        yield mock


@pytest.fixture
def mock_boot_time() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.boot_time") as mock:
        mock.return_value = datetime.now().timestamp() - 3600  # 1 hour ago
        yield mock


@pytest.fixture
def mock_hostname() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.socket.gethostname") as mock:
        mock.return_value = "test_hostname"
        yield mock


@pytest.fixture
def mock_ip_address() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.socket.gethostbyname") as mock:
        mock.return_value = "192.168.1.1"
        yield mock


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
        mock_system.return_value = "Linux"
        mock_node.return_value = "test_node"
        mock_release.return_value = "5.10"
        mock_version.return_value = "#1 SMP PREEMPT"
        mock_machine.return_value = "armv7l"
        mock_processor.return_value = "ARMv7 Processor rev 4 (v7l)"
        yield {
            "system": mock_system,
            "node": mock_node,
            "release": mock_release,
            "version": mock_version,
            "machine": mock_machine,
            "processor": mock_processor,
        }


def test_os_info(mock_platform: dict) -> None:
    expected_result = {
        "system": "Linux",
        "node": "test_node",
        "release": "5.10",
        "version": "#1 SMP PREEMPT",
        "machine": "armv7l",
        "processor": "ARMv7 Processor rev 4 (v7l)",
    }
    assert os_info() == str(expected_result)


def test_hostname(mock_hostname: MagicMock) -> None:
    assert hostname() == "test_hostname"


def test_ip_address(mock_ip_address: MagicMock) -> None:
    assert ip_address() == "192.168.1.1"


def test_uptime(mock_boot_time: MagicMock) -> None:
    assert "1:00:00" in uptime()


def test_get_running_processes(mock_process_iter: MagicMock) -> None:
    expected_result = {
        mock_process_iter.return_value[0].pid: {"pid": 1234, "name": "test_process", "username": "test_user"}
    }
    assert get_running_processes() == str(expected_result)


def test_cpu_percent(mock_cpu_percent: MagicMock) -> None:
    assert cpu_percent() == mock_cpu_percent.return_value


def test_memory_percent(mock_virtual_memory: MagicMock) -> None:
    assert memory_percent() == mock_virtual_memory.return_value.percent


def test_disk_usage(mock_disk_usage: MagicMock) -> None:
    assert disk_usage() == mock_disk_usage.return_value.percent


def test_temperature(mock_sensors_temperatures: MagicMock) -> None:
    assert temperature() == mock_sensors_temperatures.return_value["cpu_thermal"][0].current
