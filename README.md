[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!-- omit from toc -->
# Raspberry Pi AI
A Flask application with endpoints to chat with [Google's Gemini AI](https://gemini.google.com/).
Flutter is used to create a cross-platform application to interact with this API.

<!-- omit from toc -->
## Table of Contents
- [Flask Application](#flask-application)
  - [Installing Dependencies](#installing-dependencies)
  - [Getting Started](#getting-started)
  - [Testing](#testing)
  - [Linting and Formatting](#linting-and-formatting)

## Flask Application

### Installing Dependencies
Install the required dependencies using `pip`:

    pip install -e .

To install with `dev` dependencies:

    pip install -e .[dev]

### Getting Started
The Flask application can be started by executing one of the following:

    python -m rpi_ai.main
    run_rpi_ai

There are currently 2 endpoints:

- `/history`: GET chat history in form `{"messages": [{"message": <Message here>, "is_user_message": <true/false>}, ...]}`
- `/chat`: POST message to model by sending payload `{"message": <Message here>}`

### Testing
This library uses Pytest for the unit tests.
These tests are located in the `tests` directory.
To run the tests:

    python -m pytest tests

### Linting and Formatting
This library uses `ruff` for linting and formatting.

To check the code for linting errors:

    python -m ruff check .

To format the code:

    python -m ruff format .
