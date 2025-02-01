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
echo "==================================================================================================="
echo "RPi-AI has been installed successfully."
echo "The AI executable is located at: '${EXE_PATH}'"
echo "Configure the AI model: '${CONFIG_PATH}'"
echo "Add the following line to your '.bashrc' file: 'export GEMINI_API_KEY=<Your API Key>'"
echo
echo "Copy the service file to your '/etc/systemd/system' directory and enable the service:"
echo "  sudo cp ${SERVICE_PATH} /etc/systemd/system"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable ${SERVICE_FILE}"
echo "  sudo systemctl start ${SERVICE_FILE}"
echo "  sudo systemctl status ${SERVICE_FILE}"
echo
echo "To stop the service:"
echo "  sudo systemctl stop ${SERVICE_FILE}"
echo "  sudo systemctl disable ${SERVICE_FILE}"
echo "  sudo systemctl daemon-reload"
echo
echo "To view the logs:"
echo "  cat ${STDOUT_LOG}"
echo "  cat ${STDERR_LOG}"
echo
echo "To uninstall, stop the service and then:"
echo "  sudo rm /etc/systemd/system/${SERVICE_FILE}"
echo "  rm -rf ${WD}/${VENV_NAME}"
echo "  rm ${EXE_PATH}"
echo "  rm ${SERVICE_PATH}"
echo "==================================================================================================="
EOF

cat "${README_PATH}"
