import typer
import asyncio
from src.agent import ask_agent

app = typer.Typer(rich_markup_mode="markdown")

@app.command()
def ask(prompt: str):
    """🚀 Ask the agent a single question."""
    typer.echo(f"🤖 Thinking...")
    response = asyncio.run(ask_agent(prompt))
    typer.secho(f"\nAgent: {response}", fg=typer.colors.CYAN)

@app.command()
def chat():
    """💬 Start an interactive chat session."""
    typer.secho("Welcome to Universal Agent Chat! (Type "exit" or "quit" to stop)", fg=typer.colors.GREEN, bold=True)
    
    while True:
        user_input = typer.prompt("You")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = asyncio.run(ask_agent(user_input))
        typer.secho(f"Agent: {response}\n", fg=typer.colors.CYAN)

if __name__ == "__main__":
    app()