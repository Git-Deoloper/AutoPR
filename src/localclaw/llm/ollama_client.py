"""Ollama client for interacting with local LLMs"""

import requests
import json
from typing import Optional, Dict, List, Tuple
import time


class OllamaClient:
    """Client for interacting with Ollama local LLMs"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize Ollama client

        Args:
            base_url: Base URL for Ollama server (default: localhost:11434)
            model: Model to use (e.g., 'llama2', 'mistral', 'codellama', 'neural-chat')
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_generate = f"{self.base_url}/api/generate"
        self.api_tags = f"{self.base_url}/api/tags"
        self.api_pull = f"{self.base_url}/api/pull"

    def is_running(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(self.api_tags, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'].split(':')[0] for model in data.get('models', [])]
                return list(set(models))  # Remove duplicates
            return []
        except Exception as e:
            return []

    def pull_model(self, model_name: str) -> bool:
        """
        Download and install a model

        Args:
            model_name: Name of the model to pull

        Returns:
            True if successful
        """
        try:
            response = requests.post(
                self.api_pull,
                json={"name": model_name},
                timeout=300,  # 5 minute timeout for download
                stream=True
            )
            
            if response.status_code == 200:
                # Consume the stream to complete the pull
                for line in response.iter_lines():
                    pass
                return True
            return False
        except Exception as e:
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
    ) -> Tuple[str, Dict]:
        """
        Generate text using the model

        Args:
            prompt: Input prompt
            system: System message/instruction
            temperature: Sampling temperature (0-2)
            top_p: Top-p sampling parameter
            stream: Whether to stream the response

        Returns:
            Tuple of (generated_text, metadata)
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "top_p": top_p,
            }

            if system:
                payload["system"] = system

            response = requests.post(
                self.api_generate,
                json=payload,
                timeout=300,
                stream=stream
            )

            if response.status_code != 200:
                return f"Error: {response.status_code}", {"error": True}

            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            full_response += data["response"]
                        if data.get("done", False):
                            # Extract metadata from final response
                            metadata = {
                                "model": data.get("model"),
                                "total_duration": data.get("total_duration"),
                                "load_duration": data.get("load_duration"),
                                "prompt_eval_count": data.get("prompt_eval_count"),
                                "prompt_eval_duration": data.get("prompt_eval_duration"),
                                "eval_count": data.get("eval_count"),
                                "eval_duration": data.get("eval_duration"),
                            }
                            return full_response, metadata
            else:
                data = response.json()
                return data.get("response", ""), {
                    "model": data.get("model"),
                    "total_duration": data.get("total_duration"),
                    "load_duration": data.get("load_duration"),
                    "eval_count": data.get("eval_count"),
                }

        except requests.exceptions.Timeout:
            return "Error: Request timeout", {"error": True}
        except requests.exceptions.ConnectionError:
            return (
                "Error: Cannot connect to Ollama. "
                "Make sure Ollama is running: `ollama serve`",
                {"error": True}
            )
        except Exception as e:
            return f"Error: {str(e)}", {"error": True}

    def analyze_code(self, code: str, language: str = "python") -> str:
        """
        Analyze code and provide insights

        Args:
            code: Code to analyze
            language: Programming language of the code

        Returns:
            Analysis result
        """
        prompt = f"""Analyze the following {language} code and provide:
1. What it does
2. Potential bugs or issues
3. Suggestions for improvement
4. Code quality assessment

Code:
```{language}
{code}
```

Provide a concise analysis."""

        result, _ = self.generate(
            prompt,
            system="You are an expert code reviewer. Provide insightful, constructive feedback."
        )
        return result

    def fix_code(self, code: str, issue: str, language: str = "python") -> str:
        """
        Fix code based on a description of the issue

        Args:
            code: Code to fix
            issue: Description of the issue
            language: Programming language

        Returns:
            Fixed code
        """
        prompt = f"""Fix the following {language} code issue:

Issue: {issue}

Current Code:
```{language}
{code}
```

Provide the corrected code only, wrapped in ```{language}``` markers.
Do not include explanations, only the fixed code."""

        result, _ = self.generate(
            prompt,
            system="You are an expert developer. Provide only the fixed code, no explanations."
        )
        return result

    def explain_code(self, code: str, language: str = "python") -> str:
        """
        Explain what code does

        Args:
            code: Code to explain
            language: Programming language

        Returns:
            Explanation
        """
        prompt = f"""Explain what the following {language} code does:

```{language}
{code}
```

Provide a clear, concise explanation suitable for someone learning to code."""

        result, _ = self.generate(
            prompt,
            system="You are an expert educator. Explain code clearly and concisely."
        )
        return result

    def suggest_refactoring(self, code: str, language: str = "python") -> str:
        """
        Suggest refactoring improvements

        Args:
            code: Code to refactor
            language: Programming language

        Returns:
            Refactoring suggestions and improved code
        """
        prompt = f"""Suggest refactoring improvements for the following {language} code:

```{language}
{code}
```

Provide:
1. Main issues with current code
2. Suggested improvements
3. Refactored code

Focus on readability, performance, and best practices."""

        result, _ = self.generate(
            prompt,
            system="You are a senior software architect. Provide expert refactoring suggestions."
        )
        return result
