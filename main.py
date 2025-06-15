from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    InferenceClientModel,
    WebSearchTool,
    LiteLLMModel,
)

model = LiteLLMModel(model_id="anthropic/claude-4")

#web_agent = ToolCallingAgent(
#    tools=[WebSearchTool(), visit_webpage],
#    model=model,
#    max_steps=10,
#    name="web_search_agent",
#    description="Runs web searches for you.",
#)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[],
    additional_authorized_imports=[],
)

answer = manager_agent.run("What's your name ?")
