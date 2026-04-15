# 🦾 LocalClaw - Getting Started

Welcome to LocalClaw! Here's everything you need to get up and running.

## What is LocalClaw?

LocalClaw is a fully local, open-source AI code agent that:
- Runs 100% offline (no cloud, no API keys, no cost)
- Uses local LLMs like Llama2, Mistral, and CodeLlama
- Analyzes, fixes, and improves your code
- Works on Mac, Windows, and Linux

## Installation (Choose One)

### 🚀 Fastest: Docker Compose
```bash
# Clone the repo
git clone https://github.com/yourusername/localclaw.git
cd localclaw

# Start everything (Ollama + LocalClaw web UI)
docker-compose up

# In another terminal, use the CLI
localclaw analyze your-file.py

# Or open the web UI
# http://localhost:8000
```

### 📦 From Source
```bash
# Clone
git clone https://github.com/yourusername/localclaw.git
cd localclaw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e .

# Install Ollama separately from https://ollama.ai
# Then start it: ollama serve

# Download a model
ollama pull llama2

# Try it!
localclaw analyze your-file.py
```

### 🐍 Simple (Requires Ollama installed separately)
```bash
pip install -e /path/to/localclaw
localclaw --help
```

## Verify Installation

```bash
# Run verification script
bash verify-install.sh

# Or test manually
localclaw --version
localclaw setup --list-models
```

## First Run

### 1. Start Ollama
```bash
ollama serve
```
(This should stay running in a terminal)

### 2. Download a Model
```bash
# In another terminal
ollama pull llama2
# Takes 2-5 minutes depending on internet
```

### 3. Try LocalClaw

#### CLI Usage
```bash
# Analyze code
localclaw analyze script.py

# Fix a bug
localclaw fix script.py "Remove unused variable"

# Explain code
localclaw explain my_function.py

# Refactor
localclaw refactor old_code.py

# Chat with your codebase
localclaw chat ./my-project/

# Interactive chat
localclaw chat ./my-project/
# Then ask questions:
# > What does the auth module do?
# > Find security issues
# > Suggest improvements for the database layer
```

#### Web UI
```bash
# Start the web server
python -m localclaw.web.server

# Open in browser
# http://localhost:8000

# Interactive API docs
# http://localhost:8000/docs
```

## Common Commands

### Code Analysis
```bash
# Analyze a single file
localclaw analyze path/to/file.py

# Analyze with specific model
localclaw analyze file.py -m mistral

# Different language
localclaw analyze file.js -l javascript
```

### Code Fixes
```bash
# Fix a specific issue
localclaw fix file.py "Add input validation"

# Save fixed code to file
localclaw fix file.py "Improve performance" -o fixed_file.py
```

### Explain Code
```bash
# Explain what code does
localclaw explain complex_function.py

# Use different model
localclaw explain file.py -m codellama
```

### Refactoring
```bash
# Get refactoring suggestions
localclaw refactor messy_code.py

# With specific goals
localclaw refactor old_code.py -g "improve readability and performance"
```

### Interactive Chat
```bash
# Chat with entire project
localclaw chat ./my-project/

# Available commands in chat:
#   stats - Show codebase statistics
#   files - List files
#   analyze <file> - Analyze specific file
#   Or just ask questions naturally
```

### Setup/Models
```bash
# List available models
localclaw setup --list-models

# Download new model
localclaw setup -m mistral

# Check Ollama status
localclaw setup
```

## Using Different Models

LocalClaw works with any Ollama model. Popular options:

| Model | Best For | Speed | Size |
|-------|----------|-------|------|
| **llama2** (default) | General code | Medium | 4GB |
| **mistral** | Speed & quality | Fast | 4GB |
| **codellama** | Code-specific | Medium | 4GB |
| **neural-chat** | Conversations | Fast | 4GB |
| **llama2:13b** | Better analysis | Slow | 8GB |

```bash
# Try different models
ollama pull mistral
localclaw analyze file.py -m mistral

ollama pull codellama
localclaw chat ./project -m codellama
```

## REST API Usage

The web server provides REST endpoints:

```bash
# Start web server
python -m localclaw.web.server
# http://localhost:8000/docs (interactive docs)

# Analyze code via API
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"world\")",
    "language": "python"
  }'

# Load and query a codebase
curl -X POST "http://localhost:8000/api/codebase/load?path=/path/to/project"

curl -X POST http://localhost:8000/api/codebase/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does the authentication module do?"
  }'
```

## File Structure

```
localclaw/
├── README.md           # Full documentation
├── API.md              # REST API reference
├── QUICKSTART.md       # Quick start guide
├── ARCHITECTURE.md     # Technical details
├── PROJECT_SUMMARY.md  # Project overview
│
├── src/localclaw/
│   ├── cli/            # Command-line interface
│   ├── web/            # FastAPI web server
│   ├── core/           # Core functionality
│   ├── llm/            # LLM integration
│   └── config.py       # Configuration
│
├── tests/              # Test suite
├── setup.py            # Package setup
├── docker-compose.yml  # Docker setup
└── Makefile            # Development commands
```

## Useful Makefile Commands

```bash
# Development
make dev          # Install with dev tools
make test         # Run tests
make lint         # Check code quality
make format       # Auto-format code

# Running
make run-cli      # Run CLI
make run-web      # Run web server
make docker-up    # Start with Docker

# Cleanup
make clean        # Remove build artifacts
```

## Troubleshooting

### "Ollama is not running"
```bash
# Solution: Start Ollama in a new terminal
ollama serve
```

### "Model not found"
```bash
# Solution: Download the model
ollama pull llama2
# Or check available models
ollama list
```

### Slow responses
```bash
# Use a faster model
ollama pull mistral
localclaw analyze file.py -m mistral

# Or use a smaller model
# Check your system RAM usage
```

### Connection error to Ollama
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Try different base URL in .env
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### Out of memory
```bash
# Check available RAM
free -h  # Linux
vm_stat  # Mac

# Use smaller models or close other apps
# Or use Docker for isolation
docker-compose up
```

## Configuration

Create `.env` file in project directory:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama2

# Web UI Configuration  
WEB_HOST=0.0.0.0
WEB_PORT=8000
WEB_DEBUG=False

# File Reading
MAX_FILE_SIZE=1048576
```

## Next Steps

1. ✅ **Install** - Follow installation instructions above
2. ✅ **Start Ollama** - `ollama serve`
3. ✅ **Download Model** - `ollama pull llama2`
4. ✅ **Try Analyze** - `localclaw analyze README.md`
5. ✅ **Try Chat** - `localclaw chat ./localclaw/`
6. ✅ **Try Web UI** - `python -m localclaw.web.server`

## Learning Resources

- 📖 [Full README](README.md) - Complete documentation
- 🏗️ [Architecture Guide](ARCHITECTURE.md) - How it works
- 🔌 [API Reference](API.md) - REST API endpoints
- 🤝 [Contributing](CONTRIBUTING.md) - How to contribute
- 🚀 [Quick Start](QUICKSTART.md) - Another setup guide

## Getting Help

- 🐛 **Found a bug?** [Report on GitHub](https://github.com/yourusername/localclaw/issues)
- 💬 **Have questions?** [Start a discussion](https://github.com/yourusername/localclaw/discussions)
- 📧 **Need help?** Email: support@localclaw.dev

## Tips & Tricks

### Analyze Multiple Files
```bash
# Bash loop
for file in $(find . -name "*.py" -type f | head -5); do
  echo "Analyzing $file..."
  localclaw analyze "$file"
done
```

### Use in Scripts
```bash
#!/bin/bash
# Automated code review
localclaw analyze src/main.py > review.txt
localclaw fix src/main.py "Add error handling" > fixed.py
echo "Code review completed"
```

### API Usage in Python
```python
import requests

# Analyze code
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "code": "print('hello')",
        "language": "python"
    }
)
print(response.json()["result"])
```

### Custom Prompts (Advanced)
Edit `src/localclaw/llm/prompts.py` to customize prompts for your use case.

---

**You're all set! Start analyzing your code with LocalClaw! 🦾**

No API key. No cloud. No cost.
