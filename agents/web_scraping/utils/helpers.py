from agents.web_scraping.utils.types import GitHubRepository
import ast

def parse_string_to_repositories(response: str) -> list['GitHubRepository']:
    """
    Parse the string response from the agent into a list of GitHubRepository objects.
    This function assumes the response is formatted as a JSON-like string.
    """
    if isinstance(response, str):
        repositories_data = ast.literal_eval(response)
    else:
        repositories_data = response
    return [GitHubRepository(**repo) for repo in repositories_data]