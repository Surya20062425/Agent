import typer
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.agent import manager

app = typer.Typer()
console = Console()

@app.command()
def ask(prompt: str):
    """?? Ask the agent a single question."""
    console.print("[bold blue]?? Thinking...[/bold blue]")
    response = asyncio.run(manager.run(prompt))
    console.print(Panel(Markdown(response), title="Agent Response", border_style="cyan"))

@app.command()
def chat():
    """?? Start an interactive chat session."""
    console.print(Panel("[bold green]Universal Agent Shell Activated[/bold green]\nType "exit" to quit.", expand=False))
    while True:
        user_input = typer.prompt("\n[bold white]You[/bold white]")
        if user_input.lower() in ["exit", "quit"]:
            break
        console.print("[bold blue]?? Processing...[/bold blue]")
        response = asyncio.run(manager.run(user_input))
        console.print(Panel(Markdown(response), border_style="cyan"))

if __name__ == "__main__":
    app()
