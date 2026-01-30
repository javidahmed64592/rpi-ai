# Multi-stage Dockerfile for Python Template Server
# Stage 1: Backend build stage - build wheel using uv
FROM python:3.13-slim AS backend-builder

WORKDIR /build

# Install Git for dependency resolution
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy backend source files
COPY rpi_ai/ ./rpi_ai/
COPY pyproject.toml .here LICENSE README.md ./

# Build the wheel
RUN uv build --wheel

# Stage 2: Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Install Git for dependency resolution
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv in runtime stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the built wheel from backend builder
COPY --from=backend-builder /build/dist/*.whl /tmp/

# Copy configuration
COPY configuration /app/configuration/

# Install the wheel
RUN uv pip install --system --no-cache /tmp/*.whl && \
    rm /tmp/*.whl

# Create required directories
RUN mkdir -p /app/logs

# Copy included files from installed wheel to app directory
RUN SITE_PACKAGES_DIR=$(find /usr/local/lib -name "site-packages" -type d | head -1) && \
    cp "${SITE_PACKAGES_DIR}/.here" /app/.here

# Create startup script
RUN echo '#!/bin/sh\n\
    set -e\n\
    \n\
    cd /app\n\
    \n\
    # Generate API token if needed (only if not provided AND not already generated)\n\
    if [ -z "$API_TOKEN_HASH" ]; then\n\
    if [ ! -f .env ] || ! grep -q "API_TOKEN_HASH=." .env; then\n\
    echo "Generating new token..."\n\
    generate-new-token\n\
    fi\n\
    export $(grep -v "^#" .env | xargs)\n\
    fi\n\
    \n\
    exec rpi-ai' > /app/start.sh && \
    chmod +x /app/start.sh

# Expose server port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('https://localhost:$PORT/api/health', context=__import__('ssl')._create_unverified_context()).read()" || exit 1

CMD ["/app/start.sh"]
