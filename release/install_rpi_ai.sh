#!/bin/bash
set -eu

if [ -z "${GEMINI_API_KEY}" ]; then
    echo "GEMINI_API_KEY environment variable is not set. Please set it before running the script."
    exit 1
fi

WD=$(pwd)
VENV_NAME="venv"
EXE_NAME="rpi-ai"
CONFIG_FILE="ai_config.json"
LOG_FILE="rpi_ai.log"
SERVICE_FILE="rpi-ai.service"
CREATE_SERVICE_FILE="create_service.sh"
STOP_SERVICE_FILE="stop_service.sh"
UNINSTALL_FILE="uninstall_rpi_ai.sh"
README_FILE="README.txt"

CONFIG_DIR="${WD}/config"
LOGS_DIR="${WD}/logs"
SERVICE_DIR="${WD}/service"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

EXE_PATH="${WD}/${EXE_NAME}"
CONFIG_PATH="${CONFIG_DIR}/${CONFIG_FILE}"
LOG_PATH="${LOGS_DIR}/${LOG_FILE}"
SERVICE_PATH="${SERVICE_DIR}/${SERVICE_FILE}"
CREATE_SERVICE_PATH="${SERVICE_DIR}/${CREATE_SERVICE_FILE}"
STOP_SERVICE_PATH="${SERVICE_DIR}/${STOP_SERVICE_FILE}"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"
README_PATH="${WD}/${README_FILE}"

mkdir -p "${LOGS_DIR}"
mkdir -p "${SERVICE_DIR}"

echo "Creating environment '${VENV_NAME}'..."
python -m venv "${VENV_NAME}"

echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "rpi_ai-*-py3-none-any.whl")
"${BIN_DIR}/pip" install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "Creating API executable..."
cat > "${EXE_PATH}" << EOF
#!/bin/bash
export RPI_AI_PATH=${WD}
export GEMINI_API_KEY=${GEMINI_API_KEY}
"${BIN_DIR}/run_rpi_ai"
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
ReadWriteDirectories=${FULL_VENV_PATH}
ReadWriteDirectories=${LOGS_DIR}

[Install]
WantedBy=multi-user.target
EOF

echo "Creating service creation script..."
cat > "${CREATE_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

sudo cp ${SERVICE_PATH} /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_FILE}
sudo systemctl start ${SERVICE_FILE}
sudo systemctl status ${SERVICE_FILE}
EOF
chmod +x "${CREATE_SERVICE_PATH}"

echo "Creating service stop script..."
cat > "${STOP_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

sudo systemctl stop ${SERVICE_FILE}
sudo systemctl disable ${SERVICE_FILE}
sudo systemctl daemon-reload
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

sudo rm -f /etc/systemd/system/${SERVICE_FILE}
rm -rf ${WD}/${VENV_NAME}
rm -f ${EXE_PATH}
rm -f ${README_PATH}
rm -rf ${CONFIG_DIR}
rm -rf ${LOGS_DIR}
rm -rf ${SERVICE_DIR}
rm -- "\$0"
EOF
chmod +x "${UNINSTALL_PATH}"

cat > "${README_PATH}" << EOF
===================================================================================================
RPi-AI has been installed successfully.
The AI executable is located at: '${EXE_PATH}'
Configure the AI model: '${CONFIG_PATH}'
Add the following line to your '.bashrc' file: 'export GEMINI_API_KEY=<Your API Key>'

To create a start-up service for the AI, run: './${CREATE_SERVICE_FILE}'
To stop the service, run: './${STOP_SERVICE_FILE}'

To view the logs: 'cat ${LOG_PATH}'

To uninstall, run: './${UNINSTALL_FILE}'
===================================================================================================
EOF

cat "${README_PATH}"

rm -- "$0"
