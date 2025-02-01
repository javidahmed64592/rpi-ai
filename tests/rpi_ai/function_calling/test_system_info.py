from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from rpi_ai.function_calling.system_info import (
    cpu_percent,
    disk_usage,
    get_running_processes,
    memory_percent,
    temperature,
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
        mock.return_value = {"cpu_thermal": [{"current": 45.0}]}
        yield mock


@pytest.fixture
def mock_process_iter() -> Generator[MagicMock, None, None]:
    with patch("rpi_ai.function_calling.system_info.psutil.process_iter") as mock:
        mock.return_value = [Mock(info={"pid": 1234, "name": "test_process", "username": "test_user"})]
        yield mock


def test_cpu_percent(mock_cpu_percent: MagicMock) -> None:
    assert cpu_percent() == mock_cpu_percent.return_value


def test_memory_percent(mock_virtual_memory: MagicMock) -> None:
    assert memory_percent() == mock_virtual_memory.return_value.percent


def test_disk_usage(mock_disk_usage: MagicMock) -> None:
    assert disk_usage() == mock_disk_usage.return_value.percent


def test_temperature(mock_sensors_temperatures: MagicMock) -> None:
    assert temperature() == mock_sensors_temperatures.return_value["cpu_thermal"][0].current


def test_get_running_processes(mock_process_iter: MagicMock) -> None:
    expected_result = {
        mock_process_iter.return_value[0].pid: {"pid": 1234, "name": "test_process", "username": "test_user"}
    }
    assert get_running_processes() == str(expected_result)
