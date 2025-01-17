<!-- omit from toc -->
# Raspberry Pi AI UI

A Flutter application to interact with the Raspberry Pi AI.

<!-- omit from toc -->
## Table of Contents
- [Installing Dependencies](#installing-dependencies)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Linting and Formatting](#linting-and-formatting)

## Installing Dependencies
Install the required dependencies:

    flutter pub get

## Getting Started
The source code is located in the `/lib` directory.
The IP address and port on which the API is hosted can be set in the application.
The text box at the bottom allows the user to send messages to the API.

## Testing
These tests are located in the `/tests` directory.
To run the tests:

    flutter test

When adding unit tests that require mocks, generate them with the following command:

    dart run build_runner build

## Linting and Formatting
`import_sorter` is used to organise the imports across the codebase.
Run the sorter by executing:

    dart run import_sorter:main
