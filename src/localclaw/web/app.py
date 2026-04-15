"""FastAPI web application for LocalClaw."""

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from localclaw.config import config
from localclaw.core.codebase import CodebaseReader
from localclaw.llm.ollama_client import OllamaClient


# Request/Response models
class CodeInput(BaseModel):
    code: str
    language: Optional[str] = "python"
    model: Optional[str] = "llama2"


class AnalysisRequest(BaseModel):
    code: str
    language: Optional[str] = "python"
    model: Optional[str] = "llama2"


class FixRequest(BaseModel):
    code: str
    issue: str
    language: Optional[str] = "python"
    model: Optional[str] = "llama2"


class ExplanationRequest(BaseModel):
    code: str
    language: Optional[str] = "python"
    model: Optional[str] = "llama2"


class RefactoringRequest(BaseModel):
    code: str
    language: Optional[str] = "python"
    goals: Optional[str] = None
    model: Optional[str] = "llama2"


class CodebaseQuery(BaseModel):
    query: str
    model: Optional[str] = "llama2"


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="LocalClaw",
        description="A fully local, open-source AI code agent",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.WEB_ALLOWED_ORIGINS,
        allow_credentials=config.WEB_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global state
    codebase_reader = None
    current_codebase_path = None

    # Routes

    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "LocalClaw API",
            "version": "0.1.0",
            "endpoints": {
                "analyze": "/api/analyze",
                "fix": "/api/fix",
                "explain": "/api/explain",
                "refactor": "/api/refactor",
                "ollama-status": "/api/ollama/status",
                "ollama-models": "/api/ollama/models",
            }
        }

    # Ollama endpoints

    @app.get("/api/ollama/status")
    async def ollama_status():
        """Check if Ollama is running"""
        client = OllamaClient(base_url=config.OLLAMA_BASE_URL)
        return {
            "running": client.is_running(),
            "base_url": client.base_url,
        }

    @app.get("/api/ollama/models")
    async def ollama_models():
        """Get available Ollama models"""
        client = OllamaClient(base_url=config.OLLAMA_BASE_URL)
        try:
            models = client.get_available_models()
            return {
                "models": models,
                "count": len(models),
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Code analysis endpoints

    @app.post("/api/analyze")
    async def analyze(request: AnalysisRequest):
        """Analyze code"""
        try:
            client = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=request.model or config.OLLAMA_DEFAULT_MODEL,
            )

            if not client.is_running():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama is not running",
                )

            result = client.analyze_code(
                request.code,
                request.language or "python",
            )
            return {"result": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/fix")
    async def fix(request: FixRequest):
        """Fix code"""
        try:
            client = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=request.model or config.OLLAMA_DEFAULT_MODEL,
            )

            if not client.is_running():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama is not running",
                )

            result = client.fix_code(
                request.code,
                request.issue,
                request.language or "python",
            )
            return {"result": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/explain")
    async def explain(request: ExplanationRequest):
        """Explain code"""
        try:
            client = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=request.model or config.OLLAMA_DEFAULT_MODEL,
            )

            if not client.is_running():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama is not running",
                )

            result = client.explain_code(
                request.code,
                request.language or "python",
            )
            return {"result": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/refactor")
    async def refactor(request: RefactoringRequest):
        """Suggest refactoring"""
        try:
            client = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=request.model or config.OLLAMA_DEFAULT_MODEL,
            )

            if not client.is_running():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama is not running",
                )

            result = client.suggest_refactoring(
                request.code,
                request.language or "python",
            )
            return {"result": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Codebase endpoints

    @app.post("/api/codebase/load")
    async def load_codebase(path: str):
        """Load a codebase"""
        nonlocal codebase_reader, current_codebase_path

        try:
            target_path = Path(path).expanduser().resolve()
            if not target_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail="Path does not exist",
                )
            if not target_path.is_dir():
                raise HTTPException(
                    status_code=400,
                    detail="Path must be a directory",
                )

            codebase_reader = CodebaseReader(
                str(target_path),
                max_file_size=config.MAX_FILE_SIZE,
            )
            codebase_reader.read_codebase()
            current_codebase_path = str(target_path)
            stats = codebase_reader.get_stats()

            return {
                "path": current_codebase_path,
                "files": stats["total_files"],
                "lines": stats["total_lines"],
                "stats": stats,
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/codebase/summary")
    async def codebase_summary():
        """Get loaded codebase summary"""
        if not codebase_reader:
            raise HTTPException(status_code=400, detail="No codebase loaded")

        return {"summary": codebase_reader.get_summary()}

    @app.get("/api/codebase/files")
    async def codebase_files(skip: int = 0, limit: int = 50):
        """Get files from loaded codebase"""
        if not codebase_reader:
            raise HTTPException(status_code=400, detail="No codebase loaded")

        files = codebase_reader.files[skip:skip + limit]
        return {
            "files": [
                {
                    "path": f.relative_path,
                    "language": f.language,
                    "size": f.size,
                    "lines": len(f.content.split('\n'))
                }
                for f in files
            ],
            "total": len(codebase_reader.files),
            "skip": skip,
            "limit": limit,
        }

    @app.get("/api/codebase/file")
    async def codebase_file(path: str):
        """Get a specific file from codebase"""
        if not codebase_reader:
            raise HTTPException(status_code=400, detail="No codebase loaded")

        content = codebase_reader.get_file_content(path)
        if not content:
            raise HTTPException(status_code=404, detail="File not found")

        return {
            "path": path,
            "content": content,
            "lines": len(content.split('\n')),
        }

    @app.post("/api/codebase/query")
    async def codebase_query(request: CodebaseQuery):
        """Query the loaded codebase with AI"""
        if not codebase_reader:
            raise HTTPException(status_code=400, detail="No codebase loaded")

        try:
            client = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=request.model or config.OLLAMA_DEFAULT_MODEL,
            )

            if not client.is_running():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama is not running",
                )

            summary = codebase_reader.get_summary()
            prompt = f"{request.query}\n\nCodebase context:\n{summary}"

            result, _metadata = client.generate(
                prompt,
                system="You are a helpful code analysis assistant.",
            )

            return {"result": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


def run_server(
    host: str = config.WEB_HOST,
    port: int = config.WEB_PORT,
    reload: bool = False,
):
    """Run the web server"""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server()
