#!/bin/bash

# Fail on errors
set -eu

BIN_DIR="${PREFIX}/app"

echo "Unpacking RPi-AI..."
tar -xzf "${PREFIX}/rpi-ai.tar.gz" --directory="${PREFIX}"
mv "${PREFIX}/rpi-ai" "${BIN_DIR}"
rm "${PREFIX}/rpi-ai.tar.gz"

echo "Installing from wheel..."

echo "BIN_DIR:"
ls -la ${BIN_DIR}
PACKAGE_WHEEL=$(find ${BIN_DIR} -name 'rpi-ai-*-py3-none-any.whl')
"${PREFIX}/bin/pip" install "${PACKAGE_WHEEL}"
rm "${PACKAGE_WHEEL}"

echo "Creating API executable..."
"${PREFIX}/bin/create-wrappers" -t conda --bin-dir "${PREFIX}/bin" --conda-env-dir "${PREFIX}" --dest-dir "${PREFIX}/wrappers/bin"

EXEC_FILE="${BIN_DIR}/rpi-ai"
cat > $EXEC_FILE << EOF
#!/bin/bash
"${PREFIX}/wrappers/bin/run-in" python -m src.app "\$@"
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
