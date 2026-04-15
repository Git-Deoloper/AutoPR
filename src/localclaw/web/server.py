"""Web server entry point for LocalClaw"""

import click
from rich.console import Console

from localclaw.config import config
from localclaw.web.app import run_server

console = Console()


@click.command()
@click.option(
    "--host",
    default=config.WEB_HOST,
    help=f"Host to bind to (default: {config.WEB_HOST})",
)
@click.option(
    "--port",
    "-p",
    default=config.WEB_PORT,
    type=int,
    help=f"Port to run on (default: {config.WEB_PORT})",
)
@click.option("--reload", is_flag=True, help="Auto-reload on code changes")
def server(host: str, port: int, reload: bool):
    """Start LocalClaw web server"""
    console.print("[bold cyan]🚀 Starting LocalClaw Web UI[/bold cyan]")
    console.print(f"[yellow]Server:[/yellow] http://{host}:{port}")
    console.print(f"[yellow]API:[/yellow] http://{host}:{port}/docs\n")

    run_server(host=host, port=port, reload=reload)


if __name__ == "__main__":
    server()
