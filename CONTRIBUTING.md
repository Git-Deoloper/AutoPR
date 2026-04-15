# LocalClaw - Contributing Guide

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/localclaw.git
cd localclaw
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

4. Install Ollama:
- Download from [ollama.ai](https://ollama.ai)
- Start the Ollama server: `ollama serve`

5. Download a model:
```bash
localclaw setup -m llama2
```

## Project Structure

```
localclaw/
├── src/localclaw/
│   ├── core/           # Core functionality (codebase reading, file handling)
│   ├── llm/            # LLM integration (Ollama client, prompts)
│   ├── cli/            # Command-line interface
│   ├── web/            # Web UI (FastAPI application)
│   └── config.py       # Configuration management
├── tests/              # Test suite
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
├── docker-compose.yml  # Docker orchestration
└── README.md          # Documentation
```

## Development

### Running the CLI

```bash
localclaw analyze path/to/file.py
localclaw fix path/to/file.py "bug description"
localclaw explain path/to/file.py
localclaw refactor path/to/file.py
localclaw chat path/to/codebase
```

### Running the Web Server

```bash
python -m localclaw.web.server --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

### Running Tests

```bash
pytest
pytest -v  # Verbose
pytest --cov=src/localclaw  # With coverage
```

### Code Quality

```bash
# Format code
black src/localclaw tests

# Sort imports
isort src/localclaw tests

# Lint
flake8 src/localclaw tests

# Type checking
mypy src/localclaw
```

## Making Changes

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the code style

3. Write or update tests for your changes

4. Run tests and quality checks

5. Commit with clear messages:
```bash
git commit -m "feat: add feature description"
```

6. Push and create a pull request

## Adding New Commands

1. Add the command function to `src/localclaw/cli/commands.py`
2. Register it in `src/localclaw/cli/main.py`
3. Add tests in `tests/`
4. Update README with usage examples

## Adding New LLM Features

1. Add method to `OllamaClient` in `src/localclaw/llm/ollama_client.py`
2. Add prompt template to `PromptManager` in `src/localclaw/llm/prompts.py`
3. Expose via CLI command and/or web API
4. Add tests

## Questions or Issues?

Open an issue on GitHub or join our discussions!
