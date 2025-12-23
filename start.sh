#!/bin/bash

# Setup and Start Script for Flask To-Do App with PocketBase

set -e

# 1. Check and Install PocketBase
if [ ! -f "pocketbase" ]; then
    echo "PocketBase executable not found. Downloading..."
    # Note: This downloads the Linux AMD64 version.
    # For other OS, please download the appropriate version from https://github.com/pocketbase/pocketbase/releases
    curl -L -o pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v0.22.8/pocketbase_0.22.8_linux_amd64.zip
    unzip pocketbase.zip
    rm pocketbase.zip
    chmod +x pocketbase
    echo "PocketBase downloaded."
else
    echo "PocketBase already exists."
fi

# 2. Check Python Environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

# 3. Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# 4. Start PocketBase in background
echo "Starting PocketBase..."
./pocketbase serve --http=127.0.0.1:8090 > pb_output.log 2>&1 &
PB_PID=$!
echo "PocketBase started with PID $PB_PID"

# Wait for PocketBase to start
sleep 2

# 5. Start Flask App
echo "Starting Flask App..."
python app.py

# Cleanup (kill PocketBase when Flask app exits)
kill $PB_PID
