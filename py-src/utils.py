import os
from langgraph.graph import StateGraph

def print_graph(graph: StateGraph, file_name: str):
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        with open(file_name, "wb") as f:
            f.write(png_data)
    except Exception as e:
        print(f"Error saving graph to {file_name}: {e}")


__all__ = [print_graph]