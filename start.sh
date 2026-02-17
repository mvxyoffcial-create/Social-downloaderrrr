#!/bin/bash

echo "Starting Telegram Social Media Downloader Bot..."
echo "Made by @Venuboyy"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create downloads directory
mkdir -p downloads

# Start the bot
echo "Starting bot..."
python bot.py
