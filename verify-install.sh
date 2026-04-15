#!/usr/bin/env bash
# Quick test script to verify LocalClaw installation
set -e

echo "🦾 LocalClaw Installation Verification"
echo "======================================"
echo ""

# Check Python
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Check if installed
if python3 -c "import localclaw" 2>/dev/null; then
    echo "✓ LocalClaw package is installed"
else
    echo "✗ LocalClaw package not found"
    echo "  Install with: pip install -e ."
    exit 1
fi

# Check dependencies
echo ""
echo "Checking dependencies..."

dependencies=("requests" "rich" "fastapi" "click" "pydantic" "langchain")
for dep in "${dependencies[@]}"; do
    if python3 -c "import ${dep}" 2>/dev/null; then
        echo "  ✓ $dep"
    else
        echo "  ✗ $dep (missing)"
    fi
done

# Check Ollama
echo ""
echo "Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
else
    echo "⚠ Ollama is not installed"
    echo "  Install from: https://ollama.ai"
fi

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama server is running"
    
    # Check models
    models=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*' | cut -d'"' -f4 | sort -u)
    if [ -n "$models" ]; then
        echo "✓ Models available:"
        echo "$models" | sed 's/^/    - /'
    else
        echo "⚠ No models found"
        echo "  Download one: ollama pull llama2"
    fi
else
    echo "⚠ Ollama server is not running"
    echo "  Start with: ollama serve"
fi

echo ""
echo "✅ Verification complete!"
echo ""
echo "Next steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Download a model: ollama pull llama2"
echo "3. Try LocalClaw: localclaw analyze README.md"
