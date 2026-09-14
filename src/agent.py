import os
from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()

MODEL_NAME = os.getenv("DEFAULT_MODEL", "google:gemini-1.5-flash")

agent = Agent(
    MODEL_NAME,
    system_prompt=(
        "You are a Universal AI Agent. You are helpful, concise, and capable of "
        "using tools to accomplish tasks. Always verify your facts."
    ),
)

@agent.tool_plain
def get_system_status() -> str:
    """Returns the current status of the system."""
    return "System is operational. All modules are online."

async def ask_agent(prompt: str):
    """Helper function to run the agent."""
    result = await agent.run(prompt)
    return result.data