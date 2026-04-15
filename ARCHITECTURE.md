# LocalClaw Architecture

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                  LocalClaw System                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         User Interface Layer                 │  │
│  ├──────────────────────────────────────────────┤  │
│  │  CLI (Rich)      │      Web UI (FastAPI)    │  │
│  │  localclaw cmd   │      http://localhost    │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │         Application Core Layer               │  │
│  ├──────────────────────────────────────────────┤  │
│  │ CodebaseReader  │  FileHandler  │  Prompts   │  │
│  │ (Repository)    │  (I/O Ops)    │  (Templates)│  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │         LLM Integration Layer                │  │
│  ├──────────────────────────────────────────────┤  │
│  │  OllamaClient  │  LangChain Integration     │  │
│  │  (API calls)   │  (Prompt chains)           │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │         Local LLM Layer                      │  │
│  ├──────────────────────────────────────────────┤  │
│  │              Ollama Server                   │  │
│  │  (llama2, mistral, codellama, etc.)         │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Component Details

### 1. Core Module (`src/localclaw/core/`)
- **codebase.py**: `CodebaseReader` class
  - Recursively reads codebases
  - Filters by language and file size
  - Generates statistics and file trees
  - Searches and indexes files

- **file_handler.py**: `FileHandler` class
  - Read/write file operations
  - File manipulation utilities
  - Safe file operations with error handling

### 2. LLM Module (`src/localclaw/llm/`)
- **ollama_client.py**: `OllamaClient` class
  - HTTP client for Ollama API
  - Model management
  - Code analysis, fixing, explanation
  - Prompt handling and streaming

- **prompts.py**: `PromptManager` class
  - System prompts for different tasks
  - Prompt templates for various operations
  - Dynamic prompt generation

### 3. CLI Module (`src/localclaw/cli/`)
- **main.py**: Click-based CLI setup
  - Command structure
  - Entry point

- **commands.py**: Individual command implementations
  - `analyze`: Code quality analysis
  - `fix`: Bug fixing
  - `explain`: Code explanation
  - `refactor`: Refactoring suggestions
  - `chat`: Interactive codebase queries
  - `setup`: Model management

### 4. Web Module (`src/localclaw/web/`)
- **app.py**: FastAPI application
  - REST API endpoints
  - Request/response models
  - Codebase management endpoints
  - AI operation endpoints

- **server.py**: Web server runner
  - CLI wrapper for running the server
  - Configuration management

## Data Flow

### Example: Analyzing Code

```
User Input
    ↓
CLI Parsing (Click)
    ↓
FileHandler.read_file()
    ↓
OllamaClient.analyze_code()
    ↓
PromptManager.analyze_code_prompt()
    ↓
OllamaClient.generate() (HTTP POST to Ollama)
    ↓
Ollama Server (Local)
    ↓
LLM Model (e.g., llama2)
    ↓
Response Stream
    ↓
Rich Console Output
```

### Example: Chat with Codebase

```
User Query
    ↓
CodebaseReader.read_codebase()
    ↓
Generate Context (stats, file list)
    ↓
Build Prompt with Context
    ↓
OllamaClient.generate()
    ↓
Ollama Server
    ↓
LLM Model
    ↓
Streaming Response
    ↓
Interactive Output
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **CLI** | Click, Rich | Command-line interface and beautiful output |
| **Web** | FastAPI, Uvicorn | REST API and web server |
| **LLM** | Ollama, LangChain | Local model integration |
| **File I/O** | Python stdlib | File reading/writing operations |
| **Config** | python-dotenv | Environment configuration |
| **Async** | asyncio, aiofiles | Asynchronous operations |
| **Container** | Docker, docker-compose | Containerization |

## Extension Points

### Adding New Commands
1. Create function in `src/localclaw/cli/commands.py`
2. Register in `src/localclaw/cli/main.py`
3. Add REST endpoint in `src/localclaw/web/app.py`

### Adding New LLM Operations
1. Add method to `OllamaClient` in `src/localclaw/llm/ollama_client.py`
2. Create prompt template in `PromptManager`
3. Expose via CLI and/or Web API

### Adding Web UI Features
1. Add FastAPI endpoint in `src/localclaw/web/app.py`
2. Add Pydantic model for request/response
3. Document in OpenAPI (automatic from FastAPI)

## Performance Considerations

- **File Reading**: Limited to 1MB per file (configurable)
- **Streaming**: Ollama responses are streamed for faster interaction
- **Caching**: Consider caching for repeated codebase analysis
- **Memory**: Model size affects performance (7B vs 13B models)
- **GPU**: Ollama automatically uses GPU when available

## Security Considerations

- **Local Operation**: No data leaves the local machine
- **File Access**: Respects OS-level file permissions
- **Model Trust**: Only download models from official sources
- **Environment**: Sensitive config in `.env` files (not committed)

## Development Workflow

1. **Modular Design**: Each module has single responsibility
2. **Type Hints**: Used throughout for clarity
3. **Error Handling**: Comprehensive error messages
4. **Testing**: Unit tests in `tests/` directory
5. **Documentation**: Docstrings in all functions

## Future Enhancements

- [ ] Model fine-tuning support
- [ ] Multi-model comparison
- [ ] Caching layer for repeated queries
- [ ] Async streaming improvements
- [ ] VS Code extension
- [ ] Jupyter integration
- [ ] Git integration for PR analysis
- [ ] Web UI with Monaco editor
