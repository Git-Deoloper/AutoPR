"""Main CLI entry point for LocalClaw"""

import click
from functools import wraps

from localclaw.config import config
from localclaw.llm.ollama_client import OllamaError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def report_errors(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (OllamaError, OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
    return wrapped


@click.group()
@click.version_option(version="0.1.1", prog_name="LocalClaw")
def cli():
    """
    LocalClaw - A fully local, open-source AI code agent
    
    Uses your configured Ollama server; local inference after model download.
    """
    pass


# Import commands
from localclaw.cli.commands import analyze_cmd, fix_cmd, explain_cmd, refactor_cmd, chat_cmd, setup_cmd


@cli.command()
@click.argument("code_path", type=click.Path(dir_okay=False))
@click.option("--language", "-l", help="Programming language (auto-detected if not provided)")
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to use (defaults to OLLAMA_DEFAULT_MODEL)")
@report_errors
def analyze(code_path, language, model):
    """Analyze code for quality and issues"""
    analyze_cmd(code_path, language, model, console)


@cli.command()
@click.argument("code_path", type=click.Path(dir_okay=False))
@click.argument("issue", type=str)
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@report_errors
def fix(code_path, issue, language, model, output):
    """Fix code based on an issue description"""
    fix_cmd(code_path, issue, language, model, output, console)


@cli.command()
@click.argument("code_path", type=click.Path(dir_okay=False))
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to use")
@report_errors
def explain(code_path, language, model):
    """Explain what code does"""
    explain_cmd(code_path, language, model, console)


@cli.command()
@click.argument("code_path", type=click.Path(dir_okay=False))
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to use")
@click.option("--goals", "-g", help="Specific refactoring goals")
@report_errors
def refactor(code_path, language, model, goals):
    """Suggest refactoring improvements"""
    refactor_cmd(code_path, language, model, goals, console)


@cli.command()
@click.argument("codebase_path", type=click.Path(exists=True))
@click.argument("task", type=str, required=False)
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to use")
@report_errors
def chat(codebase_path, task, model):
    """Interactive chat with your codebase"""
    chat_cmd(codebase_path, task, model, console)


@cli.command()
@click.option("--model", "-m", default=lambda: config.OLLAMA_DEFAULT_MODEL, help="Model to download")
@click.option("--list-models", is_flag=True, help="List available models")
@report_errors
def setup(model, list_models):
    """Setup LocalClaw and download models"""
    setup_cmd(model, list_models, console)


if __name__ == "__main__":
    cli()
