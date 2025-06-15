from pydantic import BaseModel

class GitHubRepository(BaseModel):
    name: str
    tldr: str
    url: str
    stars: int
    forks: int