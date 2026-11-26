# Architecture

The project is a Python package under `src/localclaw/`.

| Module | Responsibility |
| --- | --- |
| `config.py` | Environment and workspace configuration |
| `core/file_handler.py` | Workspace-constrained file reads and writes |
| `core/codebase.py` | Source scanning, statistics, and bounded context selection |
| `llm/ollama_client.py` | Ollama HTTP protocol, response parsing, and task prompts |
| `llm/prompts.py` | Reusable prompt templates |
| `cli/` | Click commands and Rich terminal output |
| `web/` | FastAPI routes and server entry point |

The CLI and API share the same Ollama URL and model defaults. The client sends model parameters in Ollama's documented request format. A failed generation is not accepted as code output.

File operations resolve paths before checking the workspace boundary. The API rejects absolute paths, traversal segments, and symlink escapes. Scanning skips symlinks and `.env` variants. These checks constrain this application; they do not sandbox external processes or untrusted local filesystem users.

Codebase chat selects bounded excerpts from loaded files, favoring paths mentioned in the question. It has no embedding database, external search provider, or long-term conversation memory.

Synchronous Ollama calls run through FastAPI's threadpool routes rather than blocking its async event loop. A newly scanned codebase replaces the prior state only after its scan finishes. Codebase state is process-local and shared by clients of that server; this is a single-user development API.

Package metadata and entry points live in `pyproject.toml`. `setup.py` is a compatibility shim. The Docker composition runs the API and Ollama separately and only publishes loopback host ports.
