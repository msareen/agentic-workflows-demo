from load_llm import llm
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from utils import print_graph

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chat_bot(state: State):
    return { "messages": [llm.invoke(state["messages"])] }


graph_builder.add_node("chatbot", chat_bot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

print_graph(graph=graph,file_name="llm_with_state.png")

def printLast(response: State): 
    print(response["messages"][-1].content)
    print("==========================================")


response = graph.invoke({"messages": [{"role": "user", "content": "My name is Don" }]})
printLast(response)

#########################################

# We are executing the graph in 2 very separate context
response = graph.invoke({"messages": [{"role": "user", "content": "what is my name" }]})
printLast(response)




