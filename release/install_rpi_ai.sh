#!/bin/bash
set -eu

WD=$(pwd)
VENV_NAME="venv"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"
LOGS_DIR="${WD}/logs"
EXE_NAME="rpi-ai"
EXE_PATH="${WD}/${EXE_NAME}"

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
RPI_AI_PATH=${WD}
"${BIN_DIR}/run_rpi_ai"
EOF
chmod +x "${EXE_PATH}"

echo "==================================================================================================="
echo "RPi-AI has been installed successfully."
echo "Run the application: './rpi-ai'"
echo "Add the following line to your '.bashrc' file: 'GEMINI_API_KEY=<Your API Key>'"
echo "Configure the AI model: 'config/ai_config.json'"
echo "==================================================================================================="
