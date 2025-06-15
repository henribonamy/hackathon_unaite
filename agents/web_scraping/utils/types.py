from pydantic import BaseModel

class GitHubRepository(BaseModel):
    name: str
    authors: str
    tldr: str
    url: str
    stars: int
    last_update: str
