from smolagents import CodeAgent, WebSearchTool, LiteLLMModel
from dotenv import load_dotenv
import os
from agents.web_scraping.utils.constants import GET_REPOSITORIES_PROMPT, GET_INSTALLATION_STEPS_PROMPT
from agents.web_scraping.utils.helpers import parse_string_to_repositories
from agents.web_scraping.utils.types import GitHubRepository
from gitingest import ingest
from smolagents.monitoring import LogLevel

load_dotenv()

class WebScraperAgent:
    def __init__(self):
        self.model = LiteLLMModel(
            model_id="anthropic/claude-3-7-sonnet-20250219",
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    def get_repositories(self, user_query: str) -> list[GitHubRepository]:
        """
        **Search phase**
       • Use `WebSearchTool` to query GitHub and the web for the most relevant repositories relevant to the prompt: `${user_prompt}`.
       • For each result return the object → name, two-sentence TLDR, GitHub URL, Github stars, last updated date
        """
        prompt: str = user_query + " \n " + GET_REPOSITORIES_PROMPT
        agent: CodeAgent = CodeAgent(
            tools=[WebSearchTool()],
            model=self.model,
            stream_outputs=True
        )

        response: str = agent.run(prompt)
        print(response)

        return parse_string_to_repositories(response)

    def get_installation_steps(self, url: str) -> str:
        """
        **Ingestion phase**
           • Pass a github repo’s URL to `GitIngestTool` (wrapper around the gitingest Python package).
           • Receive: `tree`, `content`.

        **Reasoning phase**
           • From the tree & content, infer the minimal steps to **install** and **run a demo** of the project
           • Produce a shell script (macOS/Linux, Python) with conda env setup, dependency installs, with all the commands to install and run the project.
        """
        print("Ingesting repository from URL:", url)
        summary, tree, content = ingest(url, include_patterns="README.md **/README.md INSTALL.md **/INSTALL.md")
        print("Ingestion complete. Tree and content received.")

        prompt = GET_INSTALLATION_STEPS_PROMPT.replace("{tree}", tree).replace("{content}", content)

        agent: CodeAgent = CodeAgent(
            tools=[],
            model=self.model,
            stream_outputs=True
        )
        print("Running Get Installation agent")
        response: str = agent.run(prompt)

        installation_steps = f"### Infos on the repos: \n {content} \n\n ### Installation Steps:\n {response}"

        return installation_steps

