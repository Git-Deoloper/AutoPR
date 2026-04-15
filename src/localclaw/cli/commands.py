"""CLI commands for LocalClaw"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.table import Table
import time

from localclaw.core.codebase import CodebaseReader
from localclaw.core.file_handler import FileHandler
from localclaw.llm.ollama_client import OllamaClient


def _detect_language(file_path: str) -> str:
    """Detect language from file extension"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.go': 'go',
        '.rb': 'ruby',
        '.rs': 'rust',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
    }
    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, 'text')


def analyze_cmd(code_path: str, language: str, model: str, console: Console):
    """Analyze code command"""
    console.print(Panel("[bold cyan]📊 Code Analysis[/bold cyan]", expand=False))
    
    # Read file
    file_handler = FileHandler()
    try:
        code = file_handler.read_file(code_path)
    except FileNotFoundError:
        console.print("[red]Error: File not found[/red]")
        return
    
    # Detect language if not provided
    if not language:
        language = _detect_language(code_path)
    
    # Initialize Ollama client
    client = OllamaClient(model=model)
    
    # Check if Ollama is running
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Start Ollama with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    # Run analysis
    with console.status(f"[bold green]Analyzing code with {model}..."):
        result = client.analyze_code(code, language)
    
    console.print("\n[bold]Analysis Result:[/bold]")
    console.print(result)
    console.print()


def fix_cmd(code_path: str, issue: str, language: str, model: str, output: str, console: Console):
    """Fix code command"""
    console.print(Panel(f"[bold cyan]🔧 Code Fix[/bold cyan]", expand=False))
    console.print(f"[yellow]Issue:[/yellow] {issue}\n")
    
    # Read file
    file_handler = FileHandler()
    try:
        code = file_handler.read_file(code_path)
    except FileNotFoundError:
        console.print("[red]Error: File not found[/red]")
        return
    
    # Detect language if not provided
    if not language:
        language = _detect_language(code_path)
    
    # Initialize Ollama client
    client = OllamaClient(model=model)
    
    # Check if Ollama is running
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Start Ollama with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    # Run fix
    with console.status(f"[bold green]Fixing code with {model}..."):
        fixed_code = client.fix_code(code, issue, language)
    
    console.print("\n[bold]Fixed Code:[/bold]")
    
    # Extract code from markdown if present
    if f"```{language}" in fixed_code:
        fixed_code = fixed_code.split(f"```{language}")[1].split("```")[0].strip()
    elif "```" in fixed_code:
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
    
    syntax = Syntax(fixed_code, language, theme="monokai", line_numbers=True)
    console.print(syntax)
    
    # Save if output path provided
    if output:
        file_handler.write_file(output, fixed_code)
        console.print(f"\n[green]✓ Fixed code saved to {output}[/green]")
    
    console.print()


def explain_cmd(code_path: str, language: str, model: str, console: Console):
    """Explain code command"""
    console.print(Panel("[bold cyan]💡 Code Explanation[/bold cyan]", expand=False))
    
    # Read file
    file_handler = FileHandler()
    try:
        code = file_handler.read_file(code_path)
    except FileNotFoundError:
        console.print("[red]Error: File not found[/red]")
        return
    
    # Limit code length for explanation
    if len(code) > 5000:
        console.print("[yellow]Note: Code is long, showing first 5000 characters[/yellow]")
        code = code[:5000]
    
    # Detect language if not provided
    if not language:
        language = _detect_language(code_path)
    
    # Initialize Ollama client
    client = OllamaClient(model=model)
    
    # Check if Ollama is running
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Start Ollama with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    # Run explanation
    with console.status(f"[bold green]Explaining code with {model}..."):
        explanation = client.explain_code(code, language)
    
    console.print("\n[bold]Explanation:[/bold]")
    console.print(explanation)
    console.print()


def refactor_cmd(code_path: str, language: str, model: str, goals: str, console: Console):
    """Refactor code command"""
    console.print(Panel("[bold cyan]♻️  Code Refactoring[/bold cyan]", expand=False))
    
    if goals:
        console.print(f"[yellow]Goals:[/yellow] {goals}\n")
    
    # Read file
    file_handler = FileHandler()
    try:
        code = file_handler.read_file(code_path)
    except FileNotFoundError:
        console.print("[red]Error: File not found[/red]")
        return
    
    # Detect language if not provided
    if not language:
        language = _detect_language(code_path)
    
    # Initialize Ollama client
    client = OllamaClient(model=model)
    
    # Check if Ollama is running
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Start Ollama with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    # Run refactoring
    with console.status(f"[bold green]Analyzing code with {model}..."):
        result = client.suggest_refactoring(code, language)
    
    console.print("\n[bold]Refactoring Suggestions:[/bold]")
    console.print(result)
    console.print()


def chat_cmd(codebase_path: str, task: str, model: str, console: Console):
    """Interactive chat with codebase command"""
    console.print(Panel(
        "[bold cyan]💬 LocalClaw Chat[/bold cyan]\n[dim]Type 'help' for commands, 'quit' to exit[/dim]",
        expand=False
    ))
    
    # Read codebase
    try:
        reader = CodebaseReader(codebase_path)
        console.print(f"[yellow]Reading codebase from {codebase_path}...[/yellow]")
        files = reader.read_codebase()
        stats = reader.get_stats()
        console.print(f"[green]✓ Loaded {stats['total_files']} files, {stats['total_lines']:,} lines[/green]\n")
    except Exception as e:
        console.print(f"[red]Error reading codebase: {e}[/red]")
        return
    
    # Initialize Ollama client
    client = OllamaClient(model=model)
    
    # Check if Ollama is running
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Start Ollama with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    # If task provided, run it and exit
    if task:
        codebase_context = f"Codebase stats:\n{reader.get_summary()}"
        prompt = f"{task}\n\nCodebase context:\n{codebase_context}"
        
        with console.status(f"[bold green]Processing with {model}..."):
            result, _ = client.generate(
                prompt,
                system="You are a helpful code analysis assistant. Help the user understand and improve their codebase."
            )
        
        console.print(result)
        return
    
    # Interactive mode
    console.print(f"[yellow]Available models:[/yellow] {model}")
    console.print("[dim]Type your questions about the codebase:[/dim]\n")
    
    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")
        except EOFError:
            break
        
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        if user_input.lower() == "help":
            console.print(
                "[bold]Available commands:[/bold]\n"
                "  analyze <file> - Analyze a specific file\n"
                "  stats - Show codebase statistics\n"
                "  files - List files in codebase\n"
                "  quit - Exit the chat"
            )
            continue
        
        if user_input.lower() == "stats":
            console.print(reader.get_summary())
            continue
        
        if user_input.lower() == "files":
            for i, file_info in enumerate(files[:20]):
                console.print(f"  {file_info.relative_path}")
            if len(files) > 20:
                console.print(f"  ... and {len(files) - 20} more files")
            console.print()
            continue
        
        if user_input.lower().startswith("analyze "):
            file_name = user_input[8:].strip()
            file_content = reader.get_file_content(file_name)
            if file_content:
                with console.status("[bold green]Analyzing file..."):
                    analysis = client.analyze_code(file_content)
                console.print(f"[bold]Analysis of {file_name}:[/bold]")
                console.print(analysis)
            else:
                console.print(f"[red]File not found: {file_name}[/red]")
            console.print()
            continue
        
        # Regular query
        codebase_context = f"Codebase stats:\n{reader.get_summary()}\n\nFirst 10 files:\n"
        for file_info in files[:10]:
            codebase_context += f"  - {file_info.relative_path}\n"
        
        prompt = f"{user_input}\n\n{codebase_context}"
        
        with console.status("[bold green]Thinking..."):
            result, metadata = client.generate(
                prompt,
                system="You are a helpful code analysis assistant. Help the user understand and improve their codebase. Keep responses concise."
            )
        
        console.print(f"[bold cyan]Assistant:[/bold cyan] {result}\n")


def setup_cmd(model: str, list_models: bool, console: Console):
    """Setup command"""
    client = OllamaClient(model=model)
    
    if not client.is_running():
        console.print(
            "[red]Error: Ollama is not running.[/red]\n"
            "[yellow]Install Ollama from:[/yellow] [bold blue]https://ollama.ai[/bold blue]\n"
            "[yellow]Then start it with:[/yellow] [bold]ollama serve[/bold]"
        )
        return
    
    console.print(Panel("[bold cyan]🦙 LocalClaw Setup[/bold cyan]", expand=False))
    
    if list_models:
        available = client.get_available_models()
        if available:
            console.print("[bold]Available Models:[/bold]")
            for m in available:
                console.print(f"  - {m}")
        else:
            console.print("[yellow]No models found. Run 'localclaw setup -m <model>' to download one.[/yellow]")
        return
    
    # Download model
    console.print(f"[yellow]Downloading {model}...[/yellow]")
    with console.status(f"[bold green]Pulling {model}..."):
        success = client.pull_model(model)
    
    if success:
        console.print(f"[green]✓ {model} downloaded successfully![/green]")
    else:
        console.print(f"[red]Error downloading {model}[/red]")
