#!/bin/bash

# Fail on errors
set -eu

BIN_DIR="${PREFIX}/app"
mkdir -p "${BIN_DIR}"

echo "Installing from wheel..."
WHEEL_FILE=$(ls rpi_ai-*-py3-none-any.whl)
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
echo "Installation complete!"
echo "RPi-AI has been installed at: '${PREFIX}'"
echo "Add your Gemini API key to: '${ENV_FILE}'"
echo "Run RPi-AI using: '${EXEC_FILE}'"
echo "==================================================================================================="
