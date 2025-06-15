from smolagents import CodeAgent
from smolagents import CodeAgent, InferenceClientModel


class InstructionExtractorAgent:
    """Agent for extracting installation, training, and inference instructions from README files."""

    def __init__(self, max_steps: int = 10):

        self.agent = CodeAgent(
            name="readme_parser_agent",
            model=InferenceClientModel(max_tokens=64000),
            max_steps=max_steps,
            tools=[],
        )

    def extract_training_instructions(self, readme_content: str) -> str:
        prompt = f"""
        You are an expert in extracting instructions from README files.
        Given the content of a README  file, extract all the relevant commands and instructions to install a cloned git repository, train a model, and run inference on it.
        Format the output in the following structure:

        Installation instructions:
        - Step 1: <installation step>
        - Step 2: <installation step>
        - Step 3: ...
        Training instructions:
        - Step 1: <training step>
        - Step 2: <training step>
        Inference instructions:
        - Step 1: <inference step>
        Make sure to include all relevant commands, code blocks, and shell commands.

        Ignore any sections that are not related to installation, training, or inference.
        If the README does not contain any installation, training, or inference instructions, ignore them.

        Here is the content of the README file:
        {readme_content}
        """

        response = self.agent.run(prompt, stream=False)
        return response
