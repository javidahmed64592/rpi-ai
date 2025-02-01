#!/bin/bash
set -eu

WD=$(pwd)
VENV_NAME="venv"
EXE_NAME="rpi-ai"
CONFIG_FILE="ai_config.json"
STDOUT_FILE="rpi_ai.out"
STDERR_FILE="rpi_ai.err"
SERVICE_FILE="rpi-ai.service"
README_FILE="README.txt"

CONFIG_DIR="${WD}/config"
LOGS_DIR="${WD}/logs"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

EXE_PATH="${WD}/${EXE_NAME}"
CONFIG_PATH="${CONFIG_DIR}/${CONFIG_FILE}"
STDOUT_LOG="${LOGS_DIR}/${STDOUT_FILE}"
STDERR_LOG="${LOGS_DIR}/${STDERR_FILE}"
SERVICE_PATH="${WD}/${SERVICE_FILE}"
README_PATH="${WD}/${README_FILE}"

mkdir -p "${LOGS_DIR}"

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
StandardOutput=append:${STDOUT_LOG}
StandardError=append:${STDERR_LOG}

ProtectSystem=full
ReadWriteDirectories=${WD}
ReadWriteDirectories=${FULL_VENV_PATH}
ReadWriteDirectories=${LOGS_DIR}

[Install]
WantedBy=multi-user.target
EOF

cat > "${README_PATH}" << EOF
===================================================================================================
RPi-AI has been installed successfully.
The AI executable is located at: '${EXE_PATH}'
Configure the AI model: '${CONFIG_PATH}'
Add the following line to your '.bashrc' file: 'export GEMINI_API_KEY=<Your API Key>'

Copy the service file to your '/etc/systemd/system' directory and enable the service:

    sudo cp ${SERVICE_PATH} /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_FILE}
    sudo systemctl start ${SERVICE_FILE}
    sudo systemctl status ${SERVICE_FILE}

To stop the service:

    sudo systemctl stop ${SERVICE_FILE}
    sudo systemctl disable ${SERVICE_FILE}
    sudo systemctl daemon-reload

To view the logs:

    cat ${STDOUT_LOG}
    cat ${STDERR_LOG}

To uninstall, stop the service and then:

    sudo rm /etc/systemd/system/${SERVICE_FILE}
    rm -rf ${WD}/${VENV_NAME}
    rm ${EXE_PATH}
    rm ${SERVICE_PATH}
===================================================================================================
EOF

cat "${README_PATH}"
