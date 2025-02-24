[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Flutter](https://img.shields.io/badge/Flutter-3.13-02569B.svg?style=flat&logo=flutter&logoColor=white)](https://flutter.dev/)

<!-- omit from toc -->
# Raspberry Pi AI
A Flask application with endpoints to chat with [Google's Gemini AI](https://gemini.google.com/).
Flutter is used to create a cross-platform application to interact with this API.

<!-- omit from toc -->
## Table of Contents
- [Python API](#python-api)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuration](#configuration)
  - [Getting Started](#getting-started)
  - [Endpoints](#endpoints)
  - [Testing](#testing)
  - [Linting and Formatting](#linting-and-formatting)
- [Installing and Running the API](#installing-and-running-the-api)
- [Flutter Application](#flutter-application)

## Python API

### Installing Dependencies
Install the required dependencies using `pip`:

    pip install -e .

To install with `dev` dependencies:

    pip install -e .[dev]

### Configuration
Set the following environment variable before running the application:

    GEMINI_API_KEY=<Gemini API key here>

### Getting Started
The Flask application can be started by executing one of the following:

    python -m rpi_ai.main
    run_rpi_ai

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
    "model": "gemini-1.5-flash",
    "system_instruction": "You are a friendly AI assistant.",
    "candidate_count": 1,
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

### Testing
This library uses Pytest for the unit tests.
These tests are located in the `/tests` directory.
To run the tests:

    python -m pytest tests

### Linting and Formatting
This library uses `ruff` for linting and formatting.

To check the code for linting errors:

    python -m ruff check .

To format the code:

    python -m ruff format .

## Installing and Running the API
To install the API, download the release tarball and extract it.
Before running the installer, ensure you have set the `GEMINI_API_KEY` environment variable.
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
