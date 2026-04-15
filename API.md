# LocalClaw API Documentation

## REST API Endpoints

The LocalClaw web server provides a RESTful API for all operations. Access interactive documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required - fully local, no API keys needed.

## Response Format
All responses are JSON:
```json
{
  "result": "Analysis result here",
  "error": "Error message if applicable"
}
```

---

## Status & Configuration

### Check Ollama Status
```
GET /api/ollama/status
```

**Response:**
```json
{
  "running": true,
  "base_url": "http://localhost:11434"
}
```

### List Available Models
```
GET /api/ollama/models
```

**Response:**
```json
{
  "models": ["llama2", "mistral", "codellama"],
  "count": 3
}
```

---

## Code Analysis Endpoints

### Analyze Code
```
POST /api/analyze
```

**Request Body:**
```json
{
  "code": "def hello():\n    print('Hello')",
  "language": "python",
  "model": "llama2"
}
```

**Response:**
```json
{
  "result": "This function prints 'Hello' to the console..."
}
```

### Fix Code
```
POST /api/fix
```

**Request Body:**
```json
{
  "code": "def add(a, b):\n    return a + b + c",
  "issue": "NameError: variable 'c' is not defined",
  "language": "python",
  "model": "llama2"
}
```

**Response:**
```json
{
  "result": "def add(a, b):\n    return a + b"
}
```

### Explain Code
```
POST /api/explain
```

**Request Body:**
```json
{
  "code": "result = [x**2 for x in range(10)]",
  "language": "python",
  "model": "llama2"
}
```

**Response:**
```json
{
  "result": "This code creates a list of squares from 0 to 81..."
}
```

### Suggest Refactoring
```
POST /api/refactor
```

**Request Body:**
```json
{
  "code": "x = 1\ny = 2\nz = x + y\nprint(z)",
  "language": "python",
  "goals": "improve readability",
  "model": "llama2"
}
```

**Response:**
```json
{
  "result": "Current issues:\n1. Global variables\n\nSuggested improvements:\n1. Use functions..."
}
```

---

## Codebase Operations

### Load Codebase
```
POST /api/codebase/load
```

**Query Parameters:**
- `path` (string, required): Path to codebase directory

**Request:**
```
POST /api/codebase/load?path=/path/to/project
```

**Response:**
```json
{
  "path": "/path/to/project",
  "files": 42,
  "lines": 5000,
  "stats": {
    "total_files": 42,
    "total_lines": 5000,
    "by_language": {
      "python": {"files": 20, "lines": 3000},
      "javascript": {"files": 15, "lines": 1500}
    }
  }
}
```

### Get Codebase Summary
```
GET /api/codebase/summary
```

**Response:**
```json
{
  "summary": "📊 Codebase Summary\n...\nPython: 20 files, 3000 lines\n..."
}
```

### List Codebase Files
```
GET /api/codebase/files
```

**Query Parameters:**
- `skip` (integer): Number of files to skip (default: 0)
- `limit` (integer): Number of files to return (default: 50)

**Response:**
```json
{
  "files": [
    {
      "path": "src/main.py",
      "language": "python",
      "size": 1024,
      "lines": 45
    }
  ],
  "total": 42,
  "skip": 0,
  "limit": 50
}
```

### Get Specific File
```
GET /api/codebase/file
```

**Query Parameters:**
- `path` (string, required): Relative path to file in codebase

**Request:**
```
GET /api/codebase/file?path=src/main.py
```

**Response:**
```json
{
  "path": "src/main.py",
  "content": "def main():\n    ...",
  "lines": 45
}
```

### Query Codebase with AI
```
POST /api/codebase/query
```

**Request Body:**
```json
{
  "query": "What does the authentication module do?",
  "model": "llama2"
}
```

**Response:**
```json
{
  "result": "The authentication module handles user login and JWT tokens..."
}
```

---

## Common Use Cases

### 1. Analyze a File
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"world\")",
    "language": "python"
  }'
```

### 2. Fix Code Issues
```bash
curl -X POST http://localhost:8000/api/fix \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = [1, 2, 3]\ny = x[10]",
    "issue": "IndexError when accessing array",
    "language": "python"
  }'
```

### 3. Analyze Entire Codebase
```bash
# Load codebase
curl -X POST "http://localhost:8000/api/codebase/load?path=/path/to/project"

# Get summary
curl http://localhost:8000/api/codebase/summary

# Query with AI
curl -X POST http://localhost:8000/api/codebase/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main components?"
  }'
```

### 4. List and Inspect Files
```bash
# List files
curl http://localhost:8000/api/codebase/files?limit=10

# Get specific file
curl "http://localhost:8000/api/codebase/file?path=src/main.py"
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

#### 503 - Ollama Not Running
```json
{
  "detail": "Ollama is not running"
}
```

**Solution**: Start Ollama with `ollama serve`

#### 400 - No Codebase Loaded
```json
{
  "detail": "No codebase loaded"
}
```

**Solution**: Load a codebase first with `POST /api/codebase/load`

#### 404 - File Not Found
```json
{
  "detail": "File not found"
}
```

**Solution**: Check the file path with `GET /api/codebase/files`

---

## Python Client Example

```python
import requests

# Initialize
base_url = "http://localhost:8000"

# Check status
response = requests.get(f"{base_url}/api/ollama/status")
print(response.json())

# Analyze code
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

response = requests.post(
    f"{base_url}/api/analyze",
    json={
        "code": code,
        "language": "python",
        "model": "llama2"
    }
)

print(response.json()["result"])

# Load and query codebase
response = requests.post(
    f"{base_url}/api/codebase/load",
    params={"path": "/path/to/project"}
)
print(response.json())

# Query codebase
response = requests.post(
    f"{base_url}/api/codebase/query",
    json={
        "query": "What are the main modules?",
        "model": "llama2"
    }
)
print(response.json()["result"])
```

---

## Rate Limiting

Currently no rate limiting - this is a local service. Requests are limited only by:
- Ollama model processing time
- Disk I/O for file operations
- Network bandwidth (typically not a factor on localhost)

---

## CORS Support

CORS is enabled with wildcard origins (`*`), allowing requests from any domain. This is safe for local development.

---

## WebSocket Support

Currently using HTTP with streaming responses. WebSocket support planned for real-time interactions.

---

## API Versioning

Current version: v1 (implied)
- All endpoints are under `/api/`
- No breaking changes expected in near future
- Version upgrades will maintain backward compatibility

---

## Troubleshooting

### Request Times Out
- Check if Ollama is running
- Verify model is downloaded
- Check system resources (RAM, CPU)
- Try smaller model (7B instead of 13B)

### Empty Response
- Ensure code/prompt is not empty
- Check selected model exists
- Review Ollama logs for errors

### File Not Found in Codebase
- Verify file path is relative to codebase root
- Use `GET /api/codebase/files` to see available files
- Check file size (max 1MB by default)

---

## Best Practices

1. **Cache Results**: Store analysis results to avoid re-processing
2. **Use Streaming**: For large analyses, stream responses
3. **Load Context**: Load codebase once, query multiple times
4. **Choose Model**: Use appropriate model for task:
   - codellama for code-specific tasks
   - mistral for speed
   - llama2 for balanced performance
5. **Error Handling**: Always handle connection errors gracefully

---

For more help, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
