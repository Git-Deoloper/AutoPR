# AutoPR / LocalClaw

A small, open-source code assistant that connects to **your Ollama server**. Analyze a file, ask for a suggested fix, explain code, request refactoring, or query a bounded excerpt of a local codebase.

**AutoPR is the repository name. LocalClaw is the Python package and CLI command.** Both refer to this project. The package name is preserved for compatibility.

## What works

- File analysis, explanations, suggested fixes, and refactoring through the CLI.
- Codebase scanning and a simple question interface with bounded source context.
- A FastAPI JSON API with interactive documentation at `/docs`.
- Local model selection through Ollama, including full model tags.
- Workspace-constrained file access and loopback server defaults.

This is an **alpha code assistant**. It does not open pull requests, execute generated code, or automatically verify model suggestions. The web server provides an API and Swagger documentation; a separate visual editor is not included.

## Quick start

Requirements: Python **3.10+**, [Ollama](https://ollama.com/), and enough memory/disk for the model you choose. Installation and the initial model download need network access. Inference can run offline afterward when Ollama and the selected model are local. Hardware, electricity, and any remote service you configure have their own costs.

```bash
git clone https://github.com/Git-Deoloper/AutoPR.git
cd AutoPR
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

In a separate terminal, start Ollama if it is not already running:

```bash
ollama serve
```

Download a model supported by your installation; `llama2` remains the compatibility default:

```bash
localclaw setup --model llama2
localclaw setup --list-models
localclaw analyze src/localclaw/core/file_handler.py --model llama2
```

Install from this repository. A PyPI release under the `localclaw` name is **not claimed or required** by these instructions.

## Commands

```bash
localclaw analyze src/localclaw/core/file_handler.py
localclaw explain src/localclaw/core/file_handler.py
localclaw fix src/localclaw/core/file_handler.py "Explain how to handle invalid UTF-8"
localclaw refactor src/localclaw/core/file_handler.py --goals "Improve error messages"
localclaw chat . "Explain the file_handler.py workspace boundary"
localclaw chat .
```

`fix` prints a suggestion. `--output suggested.py` writes it to the selected workspace-relative file and can replace an existing file, so use a separate filename and review the diff. Model errors are reported as errors rather than saved as generated code.

Chat uses a deterministic, size-limited source selection heuristic. It favors filenames mentioned in the question; it does not provide a complete semantic index or guarantee that every relevant file fits. In interactive mode, `stats`, `files`, and `analyze <relative-path>` are available.

## Configuration

Copy `.env.example` to `.env` and edit it, or set environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server used by both CLI and API |
| `OLLAMA_DEFAULT_MODEL` | `llama2` | Used unless a command/request supplies a model |
| `WORKSPACE_ROOT` | Current working directory | Boundary for file operations and API codebase loading |
| `MAX_FILE_SIZE` | `1048576` | Maximum size of an individual scanned codebase file |
| `WEB_HOST` / `WEB_PORT` | `127.0.0.1` / `8000` | API listener |
| `WEB_ALLOWED_ORIGINS` | Localhost origins on port 8000 | Browser CORS allowlist |
| `WEB_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | Accepted HTTP Host values |

A remote `OLLAMA_BASE_URL` sends selected prompts and code to that server. Keep the default local endpoint for local inference. Codebase scanning skips symlinks, dependency/build folders, and `.env` files; review your workspace for other confidential files before asking a model to process it.

## API

```bash
python -m localclaw.web.server
```

Open **http://127.0.0.1:8000/docs**. For example:

```bash
curl http://127.0.0.1:8000/api/explain \
  -H 'Content-Type: application/json' \
  -d '{"code":"print(1 + 1)","language":"python"}'
```

See [API.md](API.md) for all routes. Codebase state belongs to one server process; this is a single-user development tool with no account/authentication system. Keep it on loopback. If changing the listener, provide your own access controls and configure the host/origin allowlists intentionally.

## Docker

```bash
docker compose up --build
# In another terminal, download the model into the Ollama service:
docker compose exec ollama ollama pull llama2
```

The Compose configuration publishes ports on `127.0.0.1` and mounts this checkout read-only as `/workspace`. The Ollama model volume persists downloads. To inspect a different project, intentionally change that read-only mount. Docker and a live Ollama model are not required for unit tests.

## Development and verification

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
localclaw --help
```

Tests exercise the Ollama request contract with mock responses, file boundaries, API behavior, and CLI errors. A successful unit test run does not measure model quality. Live inference also depends on the user's Ollama version, model, and hardware.

- [Architecture](ARCHITECTURE.md)
- [Contribution guide](CONTRIBUTING.md)
- [Report a problem](https://github.com/Git-Deoloper/AutoPR/issues)
- [MIT license](LICENSE)
