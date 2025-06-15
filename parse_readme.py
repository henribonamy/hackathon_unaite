import re


def parse_installation_steps(instructions: str):
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


if __name__ == "__main__":
    # Read readme_ultraedit.md
    with open("readme_ultraedit.md", "r") as f:
        readme_content = f.read()

    print(parse_installation_steps(readme_content))
