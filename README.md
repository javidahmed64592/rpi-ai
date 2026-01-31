[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.13/)
[![Flutter](https://img.shields.io/badge/Flutter-3.13-02569B.svg?style=flat&logo=flutter&logoColor=white)](https://flutter.dev/)
[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/rpi-ai/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/javidahmed64592/rpi-ai/actions/workflows/ci.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/javidahmed64592/rpi-ai/build.yml?branch=main&style=flat-square&label=Build&logo=github)](https://github.com/javidahmed64592/rpi-ai/actions/workflows/build.yml)
[![Docker](https://img.shields.io/github/actions/workflow/status/javidahmed64592/rpi-ai/docker.yml?branch=main&style=flat-square&label=Docker&logo=github)](https://github.com/javidahmed64592/rpi-ai/actions/workflows/docker.yml)
[![License](https://img.shields.io/github/license/javidahmed64592/rpi-ai?style=flat-square)](https://github.com/javidahmed64592/rpi-ai/blob/main/LICENSE)


<!-- omit from toc -->
# Raspberry Pi AI
A FastAPI application with endpoints to chat with [Google's Gemini AI](https://gemini.google.com/).
Flutter is used to create a cross-platform application to interact with this API.

<!-- omit from toc -->
## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Managing the Container](#managing-the-container)
- [Links](#links)
- [Flutter Application](#flutter-application)
- [License](#license)

## Prerequisites

- Docker and Docker Compose installed

## Quick Start

### Installation

Download the latest release from [GitHub Releases](https://github.com/javidahmed64592/rpi-ai/releases).

### Configuration

Rename `.env.example` to `.env` and edit it to configure the server.

- `HOST`: Server host address (default: localhost)
- `PORT`: Server port (default: 443)
- `API_TOKEN_HASH`: Leave blank to auto-generate on first run, or provide your own token hash
- `GEMINI_API_KEY`: API key from Google AI Studio

### Managing the Container

```sh
# Start the container
docker compose up -d

# Stop the container
docker compose down

# Update to the latest version
docker compose pull && docker compose up -d

# View the logs
docker compose logs -f rpi-ai
```

**Note:** You may need to add your user to the Docker group and log out/in for permission changes to take effect:
```sh
sudo usermod -aG docker ${USER}
```

## Links

- Access the web application: https://localhost:443
- Server runs at: https://localhost:443/api
- Swagger UI: https://localhost:443/api/docs
- Redoc: https://localhost:443/api/redoc

## Flutter Application
A Flutter application is created in the `/ui` directory.
This provides a GUI for interacting with the API.
See the `README.md` in the `/ui` directory for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
