import os
import yaml
import subprocess
from typing import List
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from duckduckgo_search import DDGS

load_dotenv()

class AgentManager:
    def __init__(self, config_path="config.yaml"):
        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = {
                "active_profile": "default",
                "profiles": {
                    "default": {"model": "google:gemini-1.5-flash", "temperature": 0.7}
                }
            }
        
        profile = self.config["profiles"][self.config["active_profile"]]
        self.model_name = profile["model"]
        
        self.agent = Agent(
            self.model_name,
            system_prompt=(
                "You are the Universal AI Agent. You have full access to the filesystem, "
                "the internet, and a python executor. Be precise and professional."
            ),
        )
        self._setup_tools()

    def _setup_tools(self):
        @self.agent.tool_plain
        def list_files(path: str = ".") -> str:
            """List files in the given directory."""
            try:
                return str(os.listdir(path))
            except Exception as e:
                return f"Error listing files: {e}"

        @self.agent.tool_plain
        def read_file(path: str) -> str:
            """Read content of a file."""
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"

        @self.agent.tool_plain
        def write_file(path: str, content: str) -> str:
            """Write content to a file."""
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Successfully wrote to {path}"
            except Exception as e:
                return f"Error writing file: {e}"

        @self.agent.tool_plain
        def web_search(query: str) -> str:
            """Search the internet for current information."""
            try:
                with DDGS() as ddgs:
                    results = [r["body"] for r in ddgs.text(query, max_results=3)]
                    return "\n\n".join(results) if results else "No results found."
            except Exception as e:
                return f"Search error: {e}"

        @self.agent.tool_plain
        def execute_python(code: str) -> str:
            """Execute Python code."""
            try:
                with open("temp_exec.py", "w") as f:
                    f.write(code)
                result = subprocess.run(["python", "temp_exec.py"], capture_output=True, text=True, timeout=10)
                return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            except Exception as e:
                return f"Execution error: {e}"

    async def run(self, prompt: str):
        result = await self.agent.run(prompt)
        return result.data

manager = AgentManager()
