import re
from datetime import datetime
from typing import List, Dict, Any
from smolagents import CodeAgent, LiteLLMModel
from agents.install_repo.shell_tools import ShellExecutorTool, FileSystemTool


class ProjectSetupAgent:
    """Agent that sets up GitHub projects based on installation instructions"""

    def __init__(self):
        """
        Initialize the project setup agent

        Args:
            model_name: Name of the model to use for the agent
        """
        # Initialize tools
        self.shell_tool = ShellExecutorTool()
        self.fs_tool = FileSystemTool()

        # Initialize the agent with tools
        model = LiteLLMModel(
            model_id="anthropic/claude-3-7-sonnet-latest", max_tokens=64000
        )
        self.agent = CodeAgent(
            tools=[self.shell_tool, self.fs_tool],
            model=model,
            max_steps=20,
            additional_authorized_imports=["subprocess", "os"],
        )

    def setup_project(
        self,
        repo_url: str,
        installation_instructions: str,
        project_directory: str = None,
    ) -> Dict[str, Any]:
        """
        Set up a project from a GitHub repository

        Args:
            repo_url: GitHub repository URL
            installation_instructions: Text containing installation steps
            project_directory: Directory to clone the project into

        Returns:
            Dict with setup results
        """
        # Parse the repository name from URL
        repo_name = repo_url.split("/")[-1].replace(".git", "")

        if not project_directory:
            project_directory = f"./{repo_name}"

        # Create the setup prompt
        setup_prompt = f"""
        You are a project setup assistant. Your task is to:
        
        1. Clone the GitHub repository : {repo_url}
        2. Rename the project directory to: {project_directory}
        3. Navigate to the project directory: {project_directory}
        4. Follow these installation instructions step by step:
        
        {installation_instructions}

        Warning: If the instructions do not specify to create a virtual environment, you must create one using either one of the following commands:
        1. `conda create -n {project_directory} python=3.10`
        2. `python -m venv venv`
        3. `uv venv`
        Test these methods in order from 1 to 3. Before actually running these commands, make sure these commands are available in the system.

        
        Use the shell_executor tool to run commands and filesystem tool to check files.
        Be careful and check for errors after each step.
        If a step fails, try to understand why and suggest alternatives.
        
        Start by cloning the repository.
        Ignore all the parts of the instructions that are not commands.
        Ignore all the parts of the instructions that are related to training or running the model. 
        Concatenate several commands into one command if they are related to the same step.
        """

        try:
            # Run the agent
            result = self.agent.run(setup_prompt, stream=False)

            return {
                "success": True,
                "result": result,
                "project_directory": project_directory,
                "repo_url": repo_url,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "project_directory": project_directory,
                "repo_url": repo_url,
            }


def main():
    from agents.readme_parser.parser_agent import InstructionExtractorAgent
    import json

    extract_agent = InstructionExtractorAgent()  # Create the agent
    with open("readme_diffnet.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

    example_instructions = extract_agent.extract_training_instructions(readme_content)

    agent = ProjectSetupAgent()
    # repo_url = "https://github.com/HaozheZhao/UltraEdit.git"
    repo_url = "https://github.com/nmwsharp/diffusion-net.git"

    print("Setting up project...")
    result = agent.setup_project(
        repo_url=repo_url,
        installation_instructions=example_instructions,
        project_directory=None,
    )

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # if result["success"]:
    #     print("✅ Project setup completed successfully!")
    #     print(f"Project directory: {result['project_directory']}")
    #     print(f"Setup result: {result['result']}")
    # else:
    #     print("❌ Project setup failed!")
    #     print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()
