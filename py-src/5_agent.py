from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.tools import tool

from typing import Annotated
from typing_extensions import TypedDict
from load_llm import llm
from utils import print_graph


memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


@tool("add_two_number", description="add two number")
def add_two_number(a, b):
    print("adding two number")
    ans = a + b
    return f"{ans}"


# Add notes
tools: list = [add_two_number]

llm_with_tools = llm.bind_tools(tools=tools)

tool_node = ToolNode(tools=tools)


def chatbot(state:State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def printLast(response: State): {
    print(response["messages"][-1].content)
}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
graph_builder.add_edge("tools","chatbot")

graph = graph_builder.compile(checkpointer=memory)

print_graph(graph=graph, file_name="agent.png")


response = graph.invoke({"messages": [{"role": "user", "content": "add 2 and 3" }]},config=config)

printLast(response=response)




