#!/bin/bash
echo "=================================================="
echo "  Setting up Python Virtual Environment (venv)   "
echo "=================================================="

PROJECT_DIR="/media/kishosiva/New Volume/project folder/AI_Voice_Assistant_Robot"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    echo "[VENV] Creating virtual environment at $PROJECT_DIR/venv ..."
    python3 -m venv venv
else
    echo "[VENV] Virtual environment 'venv' already exists."
fi

echo "[VENV] Activating virtual environment..."
source venv/bin/activate

echo "[VENV] Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[VENV] Virtual Environment setup completed successfully!"
