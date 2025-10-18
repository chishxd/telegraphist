#!/bin/bash

# A simple script to set up and run The Telegraphist.

echo "--- Setting up The Telegraphist ---"
echo "This may take a moment on the first run..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Create the virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null # Redirect output to keep it clean

# Run the game
echo "Setup complete. Launching The Telegraphist..."
echo "Press CTRL+C to exit the game at any time."
sleep 1
python3 main.py

# Deactivate the environment when the game is done
deactivate

echo "--- Thank you for playing! ---"