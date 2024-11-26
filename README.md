[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!-- omit from toc -->
# Template Python Repository
This repository can be used as a template for a Python application.

<!-- omit from toc -->
## Table of Contents
- [Installing Dependencies](#installing-dependencies)
- [Testing](#testing)
- [Linting and Formatting](#linting-and-formatting)

## Installing Dependencies
Install the required dependencies using `pip`:

    pip install -e .

To install with `dev` and `test` dependencies:

    pip install -e .[dev,test]

## Testing
This library uses Pytest for the unit tests.
These tests are located in the `tests` directory.
To run the tests:

    python -m pytest tests

## Linting and Formatting
This library uses `ruff` for linting and formatting.
This is configured in `ruff.toml`.

To check the code for linting errors:

    python -m ruff check .

To format the code:

    python -m ruff format .
