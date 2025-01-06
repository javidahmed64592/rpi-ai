#!/bin/bash
set -eu

echo "Creating environment 'venv'..."
python -m venv venv

echo "Installing from wheel..."
WHEEL_FILE=$(find . -name 'rpi_ai-*-py3-none-any.whl')
"venv/bin/pip" install $WHEEL_FILE
rm $WHEEL_FILE

echo "Creating API executable..."
cat > rpi-ai << EOF
#!/bin/bash
"venv/bin/python" -m rpi_ai.main
EOF
chmod +x rpi-ai

echo "Creating .env file..."
cat > .env << EOF
GEMINI_API_KEY=<Insert your Gemini API key here>
EOF

echo "==================================================================================================="
echo "RPi-AI has been installed successfully."
echo "Run the application: './rpi-ai'"
echo "Add your Gemini API key to '.env' before running the application."
echo "Configure the AI model in 'config/ai_config.json'."
echo "==================================================================================================="
