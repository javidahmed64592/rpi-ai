#!/bin/bash

# Fail on errors
set -eu

BIN_DIR="${PREFIX}/app"
mkdir -p "${BIN_DIR}"

echo "Installing from wheel..."
PACKAGE_WHEEL=$(find ${PREFIX} -name 'rpi_ai-*-py3-none-any.whl')
"${PREFIX}/bin/pip" install "${PACKAGE_WHEEL}"
rm "${PACKAGE_WHEEL}"

echo "Creating API executable..."
"${PREFIX}/bin/create-wrappers" -t conda --bin-dir "${PREFIX}/bin" --conda-env-dir "${PREFIX}" --dest-dir "${PREFIX}/wrappers/bin"

EXEC_FILE="${BIN_DIR}/rpi-ai"
cat > $EXEC_FILE << EOF
#!/bin/bash
"${PREFIX}/wrappers/bin/run-in" run_rpi_ai
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
