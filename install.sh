#!/bin/bash
# Installation script for LocalClaw

set -e

echo "🦾 LocalClaw Installation Script"
echo "================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "✗ pip is not installed. Please install Python 3.8 or later."
    exit 1
fi
echo "✓ pip is available"

# Create virtual environment if requested
if [ "$1" == "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate || . venv/Scripts/activate
    echo "✓ Virtual environment created"
fi

# Install LocalClaw
echo ""
echo "Installing LocalClaw..."
pip install -e .
echo "✓ LocalClaw installed"

# Check for Ollama
echo ""
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
else
    echo "⚠ Ollama is not installed"
    echo "  Download from: https://ollama.ai"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Download a model: ollama pull llama2"
echo "3. Try LocalClaw: localclaw --help"
