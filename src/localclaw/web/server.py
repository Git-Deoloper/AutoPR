"""Web server entry point for LocalClaw"""

import click
from rich.console import Console
from localclaw.web.app import create_app, run_server

console = Console()


@click.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
@click.option("--port", "-p", default=8000, type=int, help="Port to run on (default: 8000)")
@click.option("--reload", is_flag=True, help="Auto-reload on code changes")
def server(host: str, port: int, reload: bool):
    """Start LocalClaw web server"""
    console.print(f"[bold cyan]🚀 Starting LocalClaw Web UI[/bold cyan]")
    console.print(f"[yellow]Server:[/yellow] http://{host}:{port}")
    console.print(f"[yellow]API:[/yellow] http://{host}:{port}/docs\n")
    
    run_server(host=host, port=port, reload=reload)


if __name__ == "__main__":
    server()
