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
    choice: Literal["Angry", "Happy", "Sad", "Indifferent"]  # Use string to avoid protobuf error

class State(TypedDict):
    message: str
    condition: Optional[str]  # Must match the string return type

# ---- Graph Builder ----
graph_builder = StateGraph(State)

# ---- Nodes ----
def chat_bot(state: State):
    # LLM generates a message (plain text)
    return { "message": llm.invoke("Make a short output." + state["message"]) }

def simple_router_node(state: State):
    # Ask the LLM to classify whether the message is funny
    llm2 = llm.with_structured_output(Condition)
    print(f"LLM Generated: {state['message']}")
    
    prompt = f"""Decide the emotion of the provided message. 
    Respond with 'Angry', 'Sad', 'Happy', "Indifferent".

    Message: {state['message']}
    """
    response: Condition = llm2.invoke(prompt)
    
    match response["choice"]:
        case "Angry":
            print("😡 That's an angry message!")
        case "Happy":
            print("😄 That's a happy message!")
        case "Sad":
            print("😢 That's a sad message!")
        case "Indifferent":
            print("😐 That's an indifferent message!")

    return {
        "condition": response["choice"],
        "message": "not funny, try again" if response["choice"] == "False" else state["message"]
    }

def good_bye_node(state: State):
    print("good bye")
    return state

def joke_node(state:State):
    response = llm.invoke("Tell a joke")
    return { "message": response.content, "condition": state["condition"]  }

def poem_node(state:State):
    response = llm.invoke("Tell me a sad poem")
    return { "message": response.content, "condition": state["condition"]  }

def angry_node(state:State):
    response = llm.invoke("count to 100 to 1")
    return { "message": response.content, "condition": state["condition"]  }

# Building Graph

# ---- Add Nodes ----
# graph_builder.add_node("chatbot", chat_bot)
graph_builder.add_node("simple_route_node", simple_router_node)
graph_builder.add_node("good_bye_node", good_bye_node)
graph_builder.add_node("joke_node", joke_node)
graph_builder.add_node("poem_node", poem_node)
graph_builder.add_node("angry_node", angry_node)


# ---- Conditional Routing ----
graph_builder.add_conditional_edges(
    "simple_route_node",
    lambda state: state["condition"],
    {
        "Happy": "joke_node",
        "Sad": "poem_node",
        "Angry": "angry_node",
        "Indifferent": "good_bye_node"
    }
)

# ---- Static Edges ----
# graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge(START, "simple_route_node")
graph_builder.add_edge("joke_node", END)
graph_builder.add_edge("poem_node", END)
graph_builder.add_edge("angry_node", END)
graph_builder.add_edge("good_bye_node", END)


# ---- Compile Graph ----
graph = graph_builder.compile(checkpointer=memory)
print_graph(graph=graph, file_name="conditional_edge_3.png")

# ---- Run the Graph ----
input_state = {
    "message": "The service I have received was terrible, that was a horrible hotel"
}

graph.invoke(input_state, config=config)
