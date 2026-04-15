# Quick Start Guide for LocalClaw

## 5-Minute Setup

### Option 1: Using pip (Fastest)
```bash
# Install LocalClaw
pip install localclaw

# Start Ollama (in a new terminal)
ollama serve

# In another terminal, download a model
ollama pull llama2

# Try it out!
localclaw analyze your-file.py
```

### Option 2: Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/localclaw.git
cd localclaw

# Start everything with one command
docker-compose up

# In another terminal, use the CLI
localclaw analyze your-file.py
# Or visit http://localhost:8000 in your browser
```

### Option 3: Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/localclaw.git
cd localclaw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Start Ollama
ollama serve  # In a new terminal

# Download a model
ollama pull llama2

# Run the CLI
python -m localclaw.cli.main analyze your-file.py

# Or start the web server
python -m localclaw.web.server
# Open http://localhost:8000
```

## Installation Troubleshooting

### Issue: "Ollama is not running"
**Solution**: 
```bash
# In a new terminal, start Ollama
ollama serve
```

### Issue: "Model not found"
**Solution**:
```bash
# Download a model
ollama pull llama2
# Or try another model
ollama pull mistral
ollama pull codellama
```

### Issue: "Permission denied" on Linux/Mac
**Solution**:
```bash
# Make install script executable
chmod +x install.sh
./install.sh venv
```

### Issue: "pip: command not found"
**Solution**: Install Python 3.8 or later from [python.org](https://python.org)

## Verify Installation

```bash
# Check LocalClaw is installed
localclaw --version

# Check Ollama is running
curl http://localhost:11434/api/tags

# Check available models
ollama list

# Try analyzing a file
localclaw analyze README.md
```

## Next Steps

1. Read the [README.md](README.md) for full documentation
2. Try different models: `ollama pull codellama`
3. Start the web UI: `python -m localclaw.web.server`
4. Check out example commands in the README

## Getting Help

- 📖 [Full Documentation](https://github.com/yourusername/localclaw)
- 🐛 [Report Issues](https://github.com/yourusername/localclaw/issues)
- 💬 [Ask Questions](https://github.com/yourusername/localclaw/discussions)
- 🤝 [Contribute](CONTRIBUTING.md)

Enjoy LocalClaw! 🦾
