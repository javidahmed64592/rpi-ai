#!/bin/bash
set -eu

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

if [ -z "${GEMINI_API_KEY:-}" ]; then
    read -p "Enter Gemini API key: " GEMINI_API_KEY
    echo "GEMINI_API_KEY=${GEMINI_API_KEY}" > .env
fi

PACKAGE_NAME="rpi_ai"
WD=$(pwd)
VENV_NAME=".venv"
EXE_NAME="rpi-ai"
LOG_FILE="rpi-ai.log"
SERVICE_FILE="rpi-ai.service"
CREATE_SERVICE_FILE="start_service.sh"
STOP_SERVICE_FILE="stop_service.sh"
UNINSTALL_FILE="uninstall_rpi_ai.sh"

CONFIG_FILE="config.json"
APP_README_FILE="README.md"
SECURITY_FILE="SECURITY.md"
LICENSE_FILE="LICENSE"

CONFIG_DIR="${HOME}/.config/rpi_ai"
LOGS_DIR="${WD}/logs"
SERVICE_DIR="${WD}/service"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

EXE_PATH="${WD}/${EXE_NAME}"
LOG_PATH="${LOGS_DIR}/${LOG_FILE}"
SERVICE_PATH="${SERVICE_DIR}/${SERVICE_FILE}"
CREATE_SERVICE_PATH="${SERVICE_DIR}/${CREATE_SERVICE_FILE}"
STOP_SERVICE_PATH="${SERVICE_DIR}/${STOP_SERVICE_FILE}"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"

CONFIG_DEST="${CONFIG_DIR}/${CONFIG_FILE}"
APP_README_PATH="${WD}/${APP_README_FILE}"
LICENSE_PATH="${WD}/${LICENSE_FILE}"

echo "Creating virtual environment..."
uv venv ${VENV_NAME}

echo ${SEPARATOR}
echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "${PACKAGE_NAME}-*-py3-none-any.whl")
uv pip install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo ${SEPARATOR}
echo "Preparing directories..."
mkdir -p "${LOGS_DIR}"
mkdir -p "${SERVICE_DIR}"

SITE_PACKAGES_DIR=$(find "${FULL_VENV_PATH}/lib" -name "site-packages" -type d | head -1)
mkdir -p "${CONFIG_DIR}"
CONFIG_PATH="${SITE_PACKAGES_DIR}/configuration/${CONFIG_FILE}"

if [ -f "${CONFIG_DEST}" ]; then
    echo "AI configuration file already exists: '${CONFIG_DEST}'"
    read -p "Overwrite? (y/n): " overwrite
    if [ "${overwrite}" == "y" ]; then
        echo "Overwriting AI configuration file: '${CONFIG_DEST}'"
        mv "${CONFIG_PATH}" "${CONFIG_DEST}"
    fi
else
    echo "Creating AI configuration file: '${CONFIG_DEST}'"
    mv "${CONFIG_PATH}" "${CONFIG_DEST}"
fi

mv "${SITE_PACKAGES_DIR}/${APP_README_FILE}" "${APP_README_PATH}"
mv "${SITE_PACKAGES_DIR}/${LICENSE_FILE}" "${LICENSE_PATH}"
mv "${SITE_PACKAGES_DIR}/.here" ".here"

echo "Creating API executable..."
cat > "${EXE_PATH}" << EOF
#!/bin/bash
${BIN_DIR}/${EXE_NAME}
EOF
chmod +x "${EXE_PATH}"

echo "Creating service..."
cat > "${SERVICE_PATH}" << EOF
[Unit]
Description=Raspberry Pi AI Service
After=network.target
StartLimitBurst=5
StartLimitIntervalSec=60s

[Service]
Type=simple
User=${USER}
ExecStart=${EXE_PATH}
Restart=on-failure
RestartSec=5s
StandardOutput=append:${LOG_PATH}
StandardError=append:${LOG_PATH}

ProtectSystem=full
ReadWriteDirectories=${WD}

[Install]
WantedBy=multi-user.target
EOF

echo "Creating service creation script..."
cat > "${CREATE_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

if [ ! -f /etc/systemd/system/${SERVICE_FILE} ]; then
    echo "Creating service..."
    sudo cp ${SERVICE_PATH} /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_FILE}
fi

echo "Starting service..."
sudo systemctl start ${SERVICE_FILE}
sudo systemctl status ${SERVICE_FILE}
EOF
chmod +x "${CREATE_SERVICE_PATH}"

echo "Creating service stop script..."
cat > "${STOP_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

echo "Stopping service..."
sudo systemctl stop ${SERVICE_FILE}

read -p "Disable service? (y/n): " disable_service
if [ "\$disable_service" == "y" ]; then
    echo "Disabling service..."
    sudo systemctl disable ${SERVICE_FILE}
    sudo systemctl daemon-reload
    sudo rm -f /etc/systemd/system/${SERVICE_FILE}
fi

EOF
chmod +x "${STOP_SERVICE_PATH}"

echo "Creating uninstall script..."
cat > "${UNINSTALL_PATH}" << EOF
#!/bin/bash
set -eu

if systemctl is-active --quiet ${SERVICE_FILE}; then
    echo "Service is running. Stop the service before uninstalling."
    exit 1
fi

if [ -f /etc/systemd/system/${SERVICE_FILE} ]; then
    echo "Service is enabled. Disable the service before uninstalling."
    exit 1
fi

read -p "Remove AI configuration file? (y/n): " remove_config
if [ "\$remove_config" == "y" ]; then
    rm -f ${CONFIG_DEST}
fi

rm -rf ${VENV_NAME}
rm -rf *
EOF
chmod +x "${UNINSTALL_PATH}"

echo "${SEPARATOR}"
echo "Generating self-signed SSL certificate..."
${BIN_DIR}/generate-certificate --config="${CONFIG_DEST}"

echo "${SEPARATOR}"
echo "RPi-AI has been installed successfully."
echo
echo "Generate a new API key by running: 'uv run generate-new-token'"
echo "Run the application using: './${EXE_NAME}'"
echo
echo "Configure the application by editing: ${CONFIG_DEST}"
echo "To create a start-up service for the RPi-AI, run: './service/${CREATE_SERVICE_FILE}'"
echo "To stop the service, run: './service/${STOP_SERVICE_FILE}'"
echo "To view the logs: 'cat ${LOG_FILE}'"
echo "To uninstall, run: './${UNINSTALL_FILE}'"
echo "${SEPARATOR}"

rm -f install*
