from flask import Flask, render_template, request

from agents.readme_parser.parser_agent import InstructionExtractorAgent

from agents.install_repo.install_repo_agent import ProjectSetupAgent
from agents.readme_parser import parser_agent
from agents.web_scraping.utils.types import GitHubRepository
from agents.web_scraping.WebScraperAgent import WebScraperAgent
from manager import ResearchAssistant

app = Flask(__name__)


EXAMPLE_PAPERS = {
    "papers": [
        {
            "name": "Exemple de papier 1",
            "authors": "Auteur 1, Auteur 2",
            "tldr": "Ceci est un résumé d'exemple pour le premier papier.",
            "url": "https://example.com/paper1",
            "stars": 10,
            "forks": 100,
        },
        {
            "name": "Exemple de papier 2",
            "authors": "Auteur 3, Auteur 4",
            "tldr": "Ceci est un résumé d'exemple pour le deuxième papier.",
            "url": "https://example.com/paper2",
            "stars": 10,
            "forks": 100,
        },
        {
            "name": "Exemple de papier 2",
            "authors": "Auteur 3, Auteur 4",
            "tldr": "Ceci est un résumé d'exemple pour le deuxième papier.",
            "url": "https://example.com/paper2",
            "stars": 10,
            "forks": 100,
        },
    ]
}

webScraperAgent = WebScraperAgent()

projectSetupAgent = ProjectSetupAgent()

parserAgent = InstructionExtractorAgent()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/install_env", methods=["POST"])
def install_env():
    url = request.form.get("url")
    print("hello")
    installation_steps = webScraperAgent.get_installation_steps(url)
    installation_steps = parserAgent.extract_training_instructions(installation_steps)
    projectSetupAgent.setup_project(
        repo_url=url,
        installation_instructions=installation_steps,
        project_directory="./new_project",
    )
    return "the result of install_env"


@app.route("/get_papers", methods=["POST"])
def process():
    prompt = request.form.get("prompt")
    repositories: list[GitHubRepository] = webScraperAgent.get_repositories(prompt)
    return render_template("paper_list.html", papers=repositories)
    # return render_template("paper_list.html", papers=EXAMPLE_PAPERS["papers"])


if __name__ == "__main__":
    app.run(port=1414, debug=True)
