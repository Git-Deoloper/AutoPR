"""Regression coverage for observed protocol, isolation, and setup failures."""

import json
from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient

from localclaw.config import config
from localclaw.core.codebase import CodebaseReader
from localclaw.llm.ollama_client import OllamaClient, OllamaError
from localclaw.web.app import create_app
from localclaw.cli.main import cli


def response(data=None, lines=()):
    result = Mock(status_code=200)
    result.json.return_value = data
    result.iter_lines.return_value = [json.dumps(line).encode() for line in lines]
    return result


def test_generate_uses_ollama_non_streaming_contract(monkeypatch):
    post = Mock(return_value=response({"response": "answer", "done": True}))
    monkeypatch.setattr("localclaw.llm.ollama_client.requests.post", post)
    result, metadata = OllamaClient().generate("question", temperature=0.2, top_p=0.8)
    assert result == "answer"
    payload = post.call_args.kwargs["json"]
    assert payload["stream"] is False
    assert payload["options"] == {"temperature": 0.2, "top_p": 0.8}
    assert "temperature" not in payload


def test_streams_return_text_or_explicit_error(monkeypatch):
    monkeypatch.setattr("localclaw.llm.ollama_client.requests.post", Mock(return_value=response(lines=[
        {"response": "hello "}, {"response": "world", "done": True, "eval_count": 2}
    ])))
    assert OllamaClient().generate("question", stream=True)[0] == "hello world"
    monkeypatch.setattr("localclaw.llm.ollama_client.requests.post", Mock(return_value=response(lines=[
        {"response": "incomplete"}
    ])))
    assert OllamaClient().generate("question", stream=True)[1]["error"] is True


def test_model_tags_are_preserved(monkeypatch):
    get = Mock(return_value=response({"models": [{"name": "sample:7b"}, {"name": "sample:14b"}]}))
    monkeypatch.setattr("localclaw.llm.ollama_client.requests.get", get)
    assert OllamaClient().get_available_models() == ["sample:14b", "sample:7b"]


def test_pull_does_not_report_streamed_error_as_success(monkeypatch):
    monkeypatch.setattr("localclaw.llm.ollama_client.requests.post", Mock(return_value=response(lines=[
        {"status": "pulling"}, {"error": "model unavailable"}
    ])))
    assert OllamaClient().pull_model("missing") is False


def test_client_honors_configuration(monkeypatch):
    monkeypatch.setattr(config, "OLLAMA_BASE_URL", "http://localhost:12345")
    monkeypatch.setattr(config, "OLLAMA_DEFAULT_MODEL", "sample:7b")
    client = OllamaClient()
    assert client.base_url == "http://localhost:12345"
    assert client.model == "sample:7b"


def test_model_errors_are_not_returned_as_generated_code(monkeypatch):
    monkeypatch.setattr(OllamaClient, "generate", lambda *a, **kw: ("Error: unavailable", {"error": True}))
    with pytest.raises(OllamaError):
        OllamaClient().fix_code("print(1)", "fix it")


def test_refactor_goals_reach_model(monkeypatch):
    generate = Mock(return_value=("suggestion", {}))
    monkeypatch.setattr(OllamaClient, "generate", generate)
    OllamaClient().suggest_refactoring("print(1)", "python", "preserve public API")
    assert "preserve public API" in generate.call_args.args[0]


def test_api_rejects_symlink_escape(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()
    (outside / "private.py").write_text("private = True")
    try:
        (workspace / "shortcut").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("Symlinks unavailable on this platform")
    monkeypatch.setattr(config, "WORKSPACE_ROOT", workspace)
    client = TestClient(create_app(), base_url="http://localhost")
    assert client.post("/api/codebase/load", params={"path": "shortcut"}).status_code == 403


def test_api_reads_empty_files_and_rejects_foreign_hosts(tmp_path, monkeypatch):
    (tmp_path / "empty.py").write_text("")
    monkeypatch.setattr(config, "WORKSPACE_ROOT", tmp_path)
    client = TestClient(create_app(), base_url="http://localhost")
    assert client.post("/api/codebase/load", params={"path": "."}).status_code == 200
    result = client.get("/api/codebase/file", params={"path": "empty.py"})
    assert result.status_code == 200
    assert result.json()["content"] == ""
    assert client.get("/", headers={"host": "foreign.example"}).status_code == 400


def test_api_defaults_model_and_forwards_goals(monkeypatch):
    monkeypatch.setattr(config, "OLLAMA_DEFAULT_MODEL", "sample:14b")
    monkeypatch.setattr(OllamaClient, "is_running", lambda self: True)
    seen = {}
    def refactor(self, code, language, goals):
        seen.update(model=self.model, goals=goals)
        return "suggestion"
    monkeypatch.setattr(OllamaClient, "suggest_refactoring", refactor)
    client = TestClient(create_app(), base_url="http://localhost")
    result = client.post("/api/refactor", json={"code": "x = 1", "goals": "keep the API"})
    assert result.status_code == 200
    assert seen == {"model": "sample:14b", "goals": "keep the API"}


def test_source_context_is_bounded_and_excludes_env_files(tmp_path):
    (tmp_path / "target.py").write_text("def requested_function(): return 42")
    (tmp_path / ".env.json").write_text('{"secret": "do not load"}')
    reader = CodebaseReader(str(tmp_path))
    reader.read_codebase()
    context = reader.get_context("target.py", max_chars=1000)
    assert "requested_function" in context
    assert "do not load" not in context
    assert len(context) <= 1000


def test_cli_failure_is_nonzero_without_traceback(tmp_path, monkeypatch):
    (tmp_path / "code.py").write_text("print(1)")
    monkeypatch.setattr(config, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(OllamaClient, "is_running", lambda self: False)
    result = CliRunner().invoke(cli, ["analyze", str(tmp_path / "code.py")])
    assert result.exit_code != 0
    assert "Ollama is not running" in result.output
    assert "Traceback" not in result.output
