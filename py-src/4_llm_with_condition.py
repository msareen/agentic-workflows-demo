from load_llm import llm 
from utils import print_graph
from typing import Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# ---- Setup memory and config ----
memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}

# ---- Structured Output Schema ----
class Condition(TypedDict):
    choice: Literal["True", "False"]  # Use string to avoid protobuf error

class State(TypedDict):
    message: str
    condition: Optional[str]  # Must match the string return type

# ---- Graph Builder ----
graph_builder = StateGraph(State)

# ---- Nodes ----
def chat_bot(state: State):
    # LLM generates a message (plain text)
    return { "message": llm.invoke(state["message"]) }

def simple_router_node(state: State):
    # Ask the LLM to classify whether the message is funny
    llm2 = llm.with_structured_output(Condition)
    print(f"LLM Generated: {state['message'].content}")
    
    prompt = f"""Decide whether the following message is funny or not. 
    Respond with 'True' if it's funny, 'False' otherwise.

    Message: {state['message']}
    """
    response: Condition = llm2.invoke(prompt)
    
    if response["choice"] == "True":
        print("😄 Haa haa haa!")
    else:  
        print("😐 Not funny, try again.")

    return {
        "condition": response["choice"],
        "message": "not funny, try again" if response["choice"] == "False" else state["message"]
    }

# Building Graph

# ---- Add Nodes ----
graph_builder.add_node("chatbot", chat_bot)
graph_builder.add_node("simple_route_node", simple_router_node)

# ---- Conditional Routing ----
graph_builder.add_conditional_edges(
    "simple_route_node",
    lambda state: state["condition"],
    {
        "True": END,
        "False": "chatbot"
    }
)

# ---- Static Edges ----
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "simple_route_node")

# ---- Compile Graph ----
graph = graph_builder.compile(checkpointer=memory)
print_graph(graph=graph, file_name="conditional_edge.png")

# ---- Run the Graph ----
input_state = {
    "message": "Give me some random fact and we will see what happen next with a joke"
}

graph.invoke(input_state, config=config)
