from smolagents import (CodeAgent, InferenceClientModel, LiteLLMModel,
                        ToolCallingAgent, WebSearchTool)

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-0")

# web_agent = ToolCallingAgent(
#    tools=[WebSearchTool(), visit_webpage],
#    model=model,
#    max_steps=10,
#    name="web_search_agent",
#    description="Runs web searches for you.",
# )


class ResearchAssistant(CodeAgent):

    def __init__(self):
        super().__init__(
            tools=[], model=model, managed_agents=[], additional_authorized_imports=[]
        )

    def use(self, prompt):
        answer = self.run(prompt)
        return answer
