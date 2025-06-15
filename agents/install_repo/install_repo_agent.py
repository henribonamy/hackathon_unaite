import re
import os
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

        # LOGS
        # self.log_directory = "./logs"
        # os.makedirs(self.log_directory, exist_ok=True)

        # Initialize the agent with tools
        model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")
        self.agent = CodeAgent(
            tools=[self.shell_tool, self.fs_tool],
            model=model,
            max_steps=10,
            additional_authorized_imports=["subprocess", "os"],
        )

    def _create_log_file(self, repo_name: str) -> str:
        """
        Create a log file for the project setup

        Args:
            repo_name: Name of the repository being set up

        Returns:
            Path to the created log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"setup_{repo_name}_{timestamp}.log"
        log_path = os.path.join(self.log_directory, log_filename)

        # Create initial log entry
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Project Setup Log - {repo_name}\n")
            f.write(f"Started at: {datetime.now().isoformat()}\n")
            f.write("=" * 50 + "\n\n")

        return log_path

    def _log_stream_content(self, log_path: str, content: str):
        """
        Append stream content to log file

        Args:
            log_path: Path to the log file
            content: Content to append
        """
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(content)
            f.flush()  # Ensure content is written immediately

    def parse_installation_steps(self, instructions: str) -> List[str]:
        """
        Parse installation instructions and extract commands

        Args:
            instructions: Raw installation instructions text

        Returns:
            List of parsed commands/steps
        """
        steps = []

        # Split by common delimiters
        lines = instructions.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove markdown code block indicators
            if line.startswith("```") or line.startswith("`"):
                continue

            # Remove step numbers and bullets
            line = re.sub(r"^\d+\.\s*", "", line)
            line = re.sub(r"^[-*]\s*", "", line)

            # Skip non-command lines (descriptions, etc.)
            if any(
                line.lower().startswith(cmd)
                for cmd in [
                    "git clone",
                    "cd ",
                    "pip install",
                    "npm install",
                    "yarn install",
                    "make",
                    "cmake",
                    "python",
                    "node",
                    "apt-get",
                    "brew install",
                    "conda install",
                    "./configure",
                    "cargo install",
                    "go install",
                    "mvn",
                    "gradle",
                    "uv run",
                    "uv pip install",
                    "uv",
                ]
            ):
                steps.append(line)
            elif line.startswith("$") or line.startswith("#"):
                # Command with shell prompt
                steps.append(line.lstrip("$# "))

        return steps

    def setup_project(
        self,
        repo_url: str,
        installation_instructions: str,
        project_directory: str = None,
        use_stream: bool = False,
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

        # LOGS
        if use_stream:
            log_path = self._create_log_file(repo_name)

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
        """

        try:
            # Run the agent
            blob = self.agent.run(setup_prompt, stream=use_stream)

            if use_stream:
                result = ""
                for chunk in blob:
                    # Convert chunk to string if it's not already
                    chunk_str = str(chunk)
                    result += chunk_str

                    # LOGS
                    self._log_stream_content(log_path, chunk_str)

                completion_msg = (
                    f"\n\n"
                    + "=" * 50
                    + f"\nCompleted at: {datetime.now().isoformat()}\n"
                )
                self._log_stream_content(log_path, completion_msg)
            else:
                result = blob.to_string()

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
    """Example usage of the ProjectSetupAgent"""

    # Example installation instructions
    # example_instructions = """
    # Installation Instructions:

    # 1. install requirements: uv pip install -r requirements.txt
    # 2. install the package: uv pip install -e .
    # 3. Run the main script
    # """
    example_instructions = """
    Installation Instructions:
    
    1. pip install -r requirements
    2. cd diffusers && pip install -e .
    Training with stable-diffusion3
    Stage1 Free-form image editing
    bash scripts/run_sft_512_sd3_stage1.sh
    Stage 2: Mix training
    bash scripts/run_sft_512_with_mask_sd3_stage2.sh
    """
    # example_instructions = """
    # Installation Instructions:

    # 1. Clone the repository
    # 2. cd into the project directory
    # 3. setup a virtual environment: uv venv
    # 4. install requirements: uv pip install -r requirements.txt
    # 5. install the package: uv pip install -e .
    # 5. Run the main script: uv run main.py
    # """

    # Create the agent
    agent = ProjectSetupAgent()

    # Example GitHub repository
    repo_url = "https://github.com/HaozheZhao/UltraEdit.git"

    print("Setting up project...")
    result = agent.setup_project(
        repo_url=repo_url,
        installation_instructions=example_instructions,
        project_directory="./my_project",
        use_stream=False,
    )

    if result["success"]:
        print("✅ Project setup completed successfully!")
        print(f"Project directory: {result['project_directory']}")
        print(f"Setup result: {result['result']}")
    else:
        print("❌ Project setup failed!")
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()
