# LocalClaw - Fully Local AI Code Agent

## 🦾 LocalClaw Features

- ✨ **100% Local & Offline** - No API keys, no cloud, no cost
- 🚀 **Lightning Fast** - Runs directly on your machine
- 🔒 **Privacy First** - Your code never leaves your computer
- 🧠 **Intelligent Analysis** - Uses local LLMs (Llama, Mistral, CodeLlama)
- 📝 **Code Operations** - Analyze, fix, explain, and refactor code
- 💻 **Beautiful CLI** - Rich terminal interface with colors and styling
- 🌐 **Web UI** - FastAPI-based web interface for easy access
- 🐳 **Docker Ready** - Single `docker-compose up` to get started
- 📦 **Cross-Platform** - Works on Mac, Windows, and Linux
- 🎯 **Zero Setup** - `pip install localclaw` or download and run

## Quick Start

### Install from PyPI (Coming Soon)
```bash
pip install localclaw
```

### Or Clone and Install Locally
```bash
git clone https://github.com/Git-Deoloper/AutoPR.git
cd AutoPR
pip install -e .
```

### Setup

1. **Install Ollama**:
   - Download from [ollama.com](https://ollama.com)
   - Start it: `ollama serve`

2. **Download a Model**:
   ```bash
   localclaw setup -m llama2
   # Or: ollama pull mistral
   # Or: ollama pull codellama
   ```

3. **Start Using**:
   ```bash
   localclaw analyze path/to/your/code.py
   ```

## Usage Examples

### 🔍 Analyze Code
```bash
localclaw analyze auth.py
```

### 🔧 Fix Issues
```bash
localclaw fix auth.py "Add authentication validation"
```

### 💡 Explain Code
```bash
localclaw explain complex_algorithm.py
```

### ♻️ Refactor Code
```bash
localclaw refactor app.py --goals "improve performance and readability"
```

### 💬 Interactive Chat with Codebase
```bash
localclaw chat ./my-project/
```

Then ask questions:
```
You: What does the auth module do?
Assistant: The auth module handles user authentication...

You: Find security issues
Assistant: Found 3 potential issues:
1. SQL injection vulnerability in login...
```

### 🌐 Web UI
```bash
python -m localclaw.web.server
# Open http://localhost:8000
```

## API Endpoints

The web server provides REST API endpoints:

- `POST /api/analyze` - Analyze code
- `POST /api/fix` - Fix code based on issue description
- `POST /api/explain` - Explain what code does
- `POST /api/refactor` - Suggest refactoring improvements
- `POST /api/codebase/load` - Load a codebase for analysis
- `POST /api/codebase/query` - Query loaded codebase with AI
- `GET /api/ollama/status` - Check Ollama status
- `GET /api/ollama/models` - List available models

Full OpenAPI docs at: http://localhost:8000/docs

## Safety Defaults

- File operations now stay inside the configured workspace root instead of allowing `../` path traversal.
- The web server now binds to `127.0.0.1` by default.
- Browser access is restricted to local origins unless you explicitly expand `WEB_ALLOWED_ORIGINS`.

If you need network access from another machine or browser origin, update `.env` intentionally rather than using broad wildcard settings.

## Docker

### Using Docker Compose (Recommended)
```bash
docker-compose up
# Access at http://localhost:8000
```

### Or Build and Run Manually
```bash
docker build -t localclaw .
docker run -p 8000:8000 -p 11434:11434 localclaw
```

## Available Models

LocalClaw works with any Ollama model. Popular choices:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **llama2** | 7B | Fast | Good | General purpose |
| **mistral** | 7B | Very Fast | Good | Smaller codebase |
| **codellama** | 7B | Fast | Excellent | Code-specific |
| **neural-chat** | 7B | Fast | Good | Conversations |
| **llama2:13b** | 13B | Medium | Better | Larger projects |

Download: `ollama pull <model-name>`

## Comparison

| Feature | LocalClaw | Cursor | GitHub Copilot | Claw |
|---------|-----------|--------|---|---|
| **Local/Offline** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **API Key Required** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Cost** | 🆓 Free | 💵 $20/mo | 💵 $10/mo | 💵 Paid |
| **Open Source** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Code Privacy** | ✅ 100% | ❌ Cloud | ❌ Cloud | ❌ Cloud |
| **CLI Interface** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Web UI** | ✅ Yes | ✅ VS Code | ✅ VS Code | ✅ VS Code |
| **Codebase Analysis** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

## System Requirements

- **CPU**: Any modern processor (faster = better)
- **RAM**: 8GB minimum (16GB+ recommended)
- **Disk**: 10GB+ for models
- **OS**: macOS, Linux, Windows

### M1/M2 Mac Support
LocalClaw and Ollama have excellent Apple Silicon support:
```bash
# Ollama automatically uses GPU acceleration on M1/M2
ollama serve
```

## Advanced Usage

### Custom Models
```bash
# Run with specific model
localclaw analyze code.py -m mistral
localclaw chat ./project -m codellama
```

### Adjust Settings
Edit `.env` file:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama2
WEB_HOST=127.0.0.1
WEB_PORT=8000
WEB_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Batch Operations
```bash
# Analyze all Python files
for file in $(find . -name "*.py"); do
  localclaw analyze "$file"
done
```

## Troubleshooting

### Ollama Connection Error
```
Error: Cannot connect to Ollama. Make sure Ollama is running: `ollama serve`
```
**Solution**: Start Ollama in a new terminal: `ollama serve`

### Model Not Found
```
Error: Model 'llama2' not found
```
**Solution**: Download the model: `ollama pull llama2`

### Out of Memory
**Solution**: Use smaller model: `ollama pull mistral`

### Slow Response
**Cause**: Using CPU instead of GPU
**Solution**: 
- Ensure Ollama is using GPU acceleration
- Use a smaller model (7B instead of 13B)
- Close other applications

## Development

### Setup Development Environment
```bash
git clone https://github.com/Git-Deoloper/AutoPR.git
cd AutoPR
pip install -e ".[dev]"
pytest
```

### Run Tests
```bash
pytest
pytest -v
pytest --cov=src/localclaw
```

### Format & Lint
```bash
black src/
isort src/
flake8 src/
mypy src/
```

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Roadmap

- [ ] VS Code Extension
- [ ] Jupyter Notebook Integration
- [ ] Git Integration (auto-analyze PRs)
- [ ] Fine-tuning Support
- [ ] Team/Multi-user Support
- [ ] Better Web UI with Monaco Editor
- [ ] Model Comparison Tool
- [ ] Benchmark Suite

## License

MIT - See [LICENSE](LICENSE) for details

## Support

- 📖 [Documentation](https://github.com/yourusername/localclaw)
- 🐛 [Issue Tracker](https://github.com/yourusername/localclaw/issues)
- 💬 [Discussions](https://github.com/yourusername/localclaw/discussions)
- 📧 Email: support@localclaw.dev

---

**No API key. No cloud. No cost.**

Built with ❤️ for developers who value privacy and control.

## Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM framework
- [LangChain](https://langchain.com) - LLM utilities
- [FastAPI](https://fastapi.tiangolo.com) - Modern web framework
- [Rich](https://rich.readthedocs.io) - Beautiful terminal styling
- [Meta's Llama](https://llama.meta.com) - Open source models

---

Give us a ⭐ if you find LocalClaw useful!
