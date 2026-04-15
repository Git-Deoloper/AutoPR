"""Main CLI entry point for LocalClaw"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="LocalClaw")
def cli():
    """
    LocalClaw - A fully local, open-source AI code agent
    
    No API keys. No cloud. No cost.
    """
    pass


# Import commands
from localclaw.cli.commands import analyze_cmd, fix_cmd, explain_cmd, refactor_cmd, chat_cmd, setup_cmd


@cli.command()
@click.argument("code_path", type=click.Path(exists=True))
@click.option("--language", "-l", help="Programming language (auto-detected if not provided)")
@click.option("--model", "-m", default="llama2", help="Model to use (default: llama2)")
def analyze(code_path, language, model):
    """Analyze code for quality and issues"""
    analyze_cmd(code_path, language, model, console)


@cli.command()
@click.argument("code_path", type=click.Path(exists=True))
@click.argument("issue", type=str)
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default="llama2", help="Model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def fix(code_path, issue, language, model, output):
    """Fix code based on an issue description"""
    fix_cmd(code_path, issue, language, model, output, console)


@cli.command()
@click.argument("code_path", type=click.Path(exists=True))
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default="llama2", help="Model to use")
def explain(code_path, language, model):
    """Explain what code does"""
    explain_cmd(code_path, language, model, console)


@cli.command()
@click.argument("code_path", type=click.Path(exists=True))
@click.option("--language", "-l", help="Programming language")
@click.option("--model", "-m", default="llama2", help="Model to use")
@click.option("--goals", "-g", help="Specific refactoring goals")
def refactor(code_path, language, model, goals):
    """Suggest refactoring improvements"""
    refactor_cmd(code_path, language, model, goals, console)


@cli.command()
@click.argument("codebase_path", type=click.Path(exists=True))
@click.argument("task", type=str, required=False)
@click.option("--model", "-m", default="llama2", help="Model to use")
def chat(codebase_path, task, model):
    """Interactive chat with your codebase"""
    chat_cmd(codebase_path, task, model, console)


@cli.command()
@click.option("--model", "-m", default="llama2", help="Model to download")
@click.option("--list-models", is_flag=True, help="List available models")
def setup(model, list_models):
    """Setup LocalClaw and download models"""
    setup_cmd(model, list_models, console)


if __name__ == "__main__":
    cli()
