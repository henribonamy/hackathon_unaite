from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agents.readme_parser.parser_agent import InstructionExtractorAgent
from agents.install_repo.install_repo_agent import ProjectSetupAgent
from agents.web_scraping.utils.types import GitHubRepository
from agents.web_scraping.WebScraperAgent import WebScraperAgent

import uvicorn
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")


webScraperAgent = WebScraperAgent()
projectSetupAgent = ProjectSetupAgent()
parserAgent = InstructionExtractorAgent()

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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/install_env", response_class=HTMLResponse)
async def install_env(request: Request, url: str = Form(...)):
    print("hello")
    installation_steps = webScraperAgent.get_installation_steps(url)
    installation_steps = parserAgent.extract_training_instructions(installation_steps)
    projectSetupAgent.setup_project(
        repo_url=url,
        installation_instructions=installation_steps,
        project_directory="./new_project",
    )
    return HTMLResponse("the result of install_env")

@app.post("/get_papers", response_class=HTMLResponse)
async def get_papers(request: Request, prompt: str = Form(...)):
    repositories = webScraperAgent.get_repositories(prompt)
    # If repositories is not a list of dicts, convert as needed
    return templates.TemplateResponse("paper_list.html", {"request": request, "papers": repositories})
    # To use example papers instead, uncomment:
    # return templates.TemplateResponse("paper_list.html", {"request": request, "papers": EXAMPLE_PAPERS["papers"]})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=1414, reload=True)