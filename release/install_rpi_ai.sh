#!/bin/bash
echo "Creating environment 'rpi_ai_venv'..."
python -m venv rpi_ai_venv
source rpi_ai_venv/bin/activate

echo "Installing from wheel..."
pip install rpi_ai-*-py3-none-any.whl
rm rpi_ai-*-py3-none-any.whl

echo "Creating API executable..."
cat > rpi-ai << EOF
#!/bin/bash
"rpi_ai_venv/bin/python" -m rpi_ai.main
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
