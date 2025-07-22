from langgraph.prebuilt import create_react_agent

from load_llm import llm
from utils import print_graph

def tool() -> None:
    """Testing tool."""
    ...

agent = create_react_agent(
    llm,
    tools=[tool],
)

print_graph(graph=agent,file_name="./prebuilt-agent.png")
agent.get_graph().draw_mermaid_png()