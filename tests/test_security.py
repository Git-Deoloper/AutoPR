"""Security-focused tests for LocalClaw."""

import sys
from pathlib import Path

import pytest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from localclaw.core.file_handler import FileHandler  # noqa: E402
from localclaw.web.app import create_app  # noqa: E402


def test_file_handler_blocks_path_traversal(tmp_path):
    """File operations must stay inside the configured base path."""
    handler = FileHandler(str(tmp_path))

    with pytest.raises(ValueError):
        handler.read_file("../outside.txt")

    with pytest.raises(ValueError):
        handler.write_file("../outside.txt", "blocked")


def test_web_app_restricts_default_cors_origin():
    """The API should not allow wildcard browser origins by default."""
    app = create_app()
    cors = next(
        middleware
        for middleware in app.user_middleware
        if middleware.cls is CORSMiddleware
    )

    assert cors.kwargs["allow_origins"] != ["*"]
    assert "http://localhost:8000" in cors.kwargs["allow_origins"]


def test_load_codebase_rejects_file_paths(tmp_path):
    """Only directories should be accepted as codebase roots."""
    app = create_app()
    client = TestClient(app)
    target = tmp_path / "single_file.py"
    target.write_text("print('hello')", encoding="utf-8")

    response = client.post("/api/codebase/load", params={"path": str(target)})

    assert response.status_code == 400
    assert response.json()["detail"] == "Path must be a directory"
