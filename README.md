[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Flutter](https://img.shields.io/badge/Flutter-3.13-02569B.svg?style=flat&logo=flutter&logoColor=white)](https://flutter.dev/)
[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/rpi-ai/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/javidahmed64592/rpi-ai/actions)
[![License](https://img.shields.io/github/license/javidahmed64592/rpi-ai?style=flat-square)](https://github.com/javidahmed64592/rpi-ai/blob/main/LICENSE)


<!-- omit from toc -->
# Raspberry Pi AI
A Flask application with endpoints to chat with [Google's Gemini AI](https://gemini.google.com/).
Flutter is used to create a cross-platform application to interact with this API.

<!-- omit from toc -->
## Table of Contents
- [Python API](#python-api)
  - [uv](#uv)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuration](#configuration)
  - [Getting Started](#getting-started)
  - [Endpoints](#endpoints)
  - [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)
- [Installing and Running the API](#installing-and-running-the-api)
- [Flutter Application](#flutter-application)
- [License](#license)

## Python API

### uv

This repository is managed using the `uv` Python project manager: https://docs.astral.sh/uv/

To install `uv`:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh                                    # Linux/Mac
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

### Installing Dependencies

Install the required dependencies using `uv`:

```sh
uv sync
```

To install with development dependencies:

```sh
uv sync --extra dev
```

### Configuration
Set the following environment variable before running the application:

```sh
    GEMINI_API_KEY=<Gemini API key here>
```

### Getting Started
The Flask application can be started by executing:

```sh
    uv run rpi-ai
```

### Endpoints
When the API is started, an authorisation token is generated which is required to authenticate requests.
Requests must have the following header:

```json
{
    "Authorization": "<Authorisation token here>",
}
```

`/`: GET method, check if the server is alive and return payload:
```json
{
    "status": "alive"
}
```

`/login`: GET method, start new chat and return payload:
```json
{
    "message": "<First message>",
    "is_user_message": false
}
```

`/get-config`: GET method, retrieve the current AI configuration and return payload:
```json
{
    "model": "gemini-2.0-flash",
    "system_instruction": "You are a friendly AI assistant.",
    "max_output_tokens": 1000,
    "temperature": 1.0
}
```

`/update-config`: POST method, update the AI configuration by sending request with new config data and return payload:
```json
{
    "message": "<First message after config update>",
    "is_user_message": false
}
```

`/chat`: POST method, send message to model by sending request:
```json
{
    "message": "<Message here>"
}
```
and return payload:
```json
{
    "message": "<Model response>",
    "is_user_message": false
}
```

`/send-audio`: POST method, send voice message to model by sending request with file:
```json
{
    "audio": "<Audio bytes here>"
}
```
and return payload:
```json
{
    "text": "<Model response>",
    "bytes": "<Audio bytes>"
}
```

### Testing, Linting, and Type Checking

- **Run tests:** `uv run pytest`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`

## Installing and Running the API
To install the API, download the release tarball and extract it.
Run the `install_rpi_ai.sh` script:

    tar -xzf rpi_ai.tar.gz
    rm rpi_ai.tar.gz
    cd rpi_ai
    ./install_rpi_ai.sh

This script will create a virtual environment, install the API from the wheel file, and set up the necessary directories and files.

To create a start-up service for the API, run the `start_service.sh` script:

    ./service/start_service.sh

This will create and start a systemd service that runs the API on system start-up.

To stop the service, run the `stop_service.sh` script:

    ./service/stop_service.sh

To uninstall the API, run the `uninstall_rpi_ai.sh` script:

    ./uninstall_rpi_ai.sh
    cd ..
    rm -rf rpi_ai

This will remove the virtual environment, executable, and all related files and directories.
The folder can then safely be deleted.

## Flutter Application
A Flutter application is created in the `/ui` directory.
This provides a GUI for interacting with the API.
See the `README.md` in the `/ui` directory for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
