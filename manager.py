from smolagents import (CodeAgent, InferenceClientModel, LiteLLMModel,
                        ToolCallingAgent, WebSearchTool)

from agents.web_scraping.WebScraperAgent import WebScraperAgent


class ResearchAssistant(CodeAgent):

    def __init__(self):
        manager = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")
        webScraperAgent = WebScraperAgent()
        super().__init__(
            tools=[],
            model=manager,
            managed_agents=[webScraperAgent],
            additional_authorized_imports=[],
        )

    def use(self, prompt):
        answer = self.run(prompt)
        return answer
