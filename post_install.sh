#!/bin/bash

# Fail on errors
set -eu

BIN_DIR="${PREFIX}/app"

echo "Installing from wheel..."
WHEEL_FILE=$(ls rpi-ai-*-py3-none-any.whl)
"${PREFIX}/bin/pip" install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "Creating API executable..."
"${PREFIX}/bin/create-wrappers" -t conda --bin-dir "${PREFIX}/bin" --conda-env-dir "${PREFIX}" --dest-dir "${PREFIX}/wrappers/bin"

EXEC_FILE="${BIN_DIR}/rpi-ai"
cat > $EXEC_FILE << EOF
#!/bin/bash
"${PREFIX}/wrappers/bin/run-in" python -m run_rpi_ai
EOF
chmod +x $EXEC_FILE

echo "Creating .env file..."
ENV_FILE="${BIN_DIR}/.env"
cat > $ENV_FILE << EOF
GEMINI_API_KEY=<Insert your Gemini API key here>
EOF

echo "==================================================================================================="
echo "RPi-AI has been installed successfully at: '${PREFIX}'"
echo "The launchers are located at: '${BIN_DIR}'"
echo "Add your Gemini API key to '${ENV_FILE}' before running the application."
echo "==================================================================================================="
