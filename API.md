# AutoPR / LocalClaw API

Start with `python -m localclaw.web.server`, then open http://127.0.0.1:8000/docs for the generated request schema. This is a single-user local API without authentication. See the [README](README.md#configuration) for workspace and listener settings.

## Routes

| Method | Path | Input | Output |
| --- | --- | --- | --- |
| GET | `/` | None | Version, workspace, and endpoint information |
| GET | `/api/ollama/status` | None | Whether the configured Ollama endpoint responds |
| GET | `/api/ollama/models` | None | Installed model names, including tags |
| POST | `/api/analyze` | JSON `code`, optional `language`, `model` | `result` text |
| POST | `/api/fix` | JSON `code`, `issue`, optional `language`, `model` | Suggested code as `result` text |
| POST | `/api/explain` | JSON `code`, optional `language`, `model` | `result` text |
| POST | `/api/refactor` | JSON `code`, optional `language`, `model`, `goals` | `result` text |
| POST | `/api/codebase/load` | Query parameter `path` relative to `WORKSPACE_ROOT` | Scan statistics |
| GET | `/api/codebase/summary` | None | Loaded codebase summary |
| GET | `/api/codebase/files` | Optional query `skip` (>=0), `limit` (1–200) | File metadata page |
| GET | `/api/codebase/file` | Query `path` relative to loaded codebase | File text, including empty files |
| POST | `/api/codebase/query` | JSON `query`, optional `model` | Answer based on bounded source excerpts |

Omitted or null model values use `OLLAMA_DEFAULT_MODEL`. Language defaults to Python. API operations return suggestions; they do not write or execute model output.

## Load and query

```bash
curl -X POST 'http://127.0.0.1:8000/api/codebase/load?path=src'
curl http://127.0.0.1:8000/api/codebase/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"Explain core/file_handler.py"}'
```

An unavailable Ollama server returns 503. Invalid or outside-workspace paths return 400/403; missing paths/files return 404. Upstream generation errors fail the request. Scan results and selected excerpts are bounded by the behavior described in the README; they are not a semantic index.

## Ollama protocol reference

The client uses the [official generation API](https://docs.ollama.com/api/generate): `stream` is explicitly sent in the JSON payload, and sampling parameters are inside `options`.
