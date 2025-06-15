from agents.web_scraping.WebScraperAgent import WebScraperAgent
from agents.web_scraping.utils.types import GitHubRepository

user_query: str = "I want to test locally recent open-source project of image generation. For example look at https://github.com/HaozheZhao/UltraEdit"

webScraperAgent = WebScraperAgent()
repositories: list[GitHubRepository] = webScraperAgent.get_repositories(user_query)

# print("-------- Repositories fetched --------")
for repo in repositories:
    print("\n\n")
    print(repo)

# selected_repository = repositories[0]  # Assuming the user selects the first repository
#
# print("-------- Fetching specific repository installation guide --------")
# installation_steps: str = webScraperAgent.get_installation_steps("https://github.com/HaozheZhao/UltraEdit")
#
# print(installation_steps)




