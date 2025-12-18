#!/bin/bash
# Setup script for Claude Project Chat

set -e

echo "Setting up Claude Project Chat..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "Using Python $PYTHON_VERSION"

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Upgrade pip
echo "Upgrading pip..."
./venv/bin/pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "Please edit .env with your credentials"
    fi
fi

# Create uploads directory if it doesn't exist
mkdir -p static/uploads

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your credentials (API key or Claude cookie)"
echo "  2. Run the app with: ./venv/bin/python app.py"
echo "     Or activate venv first: source venv/bin/activate && python app.py"
echo ""
