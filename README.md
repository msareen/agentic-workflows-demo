
# Agent Demo Project

This project demonstrates building and running AI agents using LangGraph, LangChain, and FastAPI. Each Python file is an independent demo and can be run directly as a script—Jupyter notebooks are provided for convenience but are completely optional.

## Project Structure

- `main.py` — Standalone demo script.
- `pyproject.toml` — Project dependencies and configuration.
- `simple/` — Contains independent demo files:
  - `agent_with_state.ipynb` — (Optional) Jupyter notebook for stateful agent demos.
  - `agent_with_condition.ipynb` — (Optional) Notebook for conditional agent flows.
  - `agent.ipynb` — (Optional) Basic agent notebook.
  - `load_env.py` — Loads environment variables for API keys.
  - `load_llm.py` — Shared package file for loading and configuring the language model.
  - `utils.py` — Shared package file for utility functions (e.g., graph visualization, tracing).
  - `5_agent.py`, `fast_api.py`, etc. — Each is a standalone demo and can be run directly with Python.
- `server/` — Contains API server code (e.g., `api.py`).

## Step-by-Step LLM Demos

The project is organized to help you build LLM-powered agents step by step. Each file demonstrates a different concept or feature. You can run any `.py` file directly:

```sh
python simple/5_agent.py
```

Jupyter notebooks are available for interactive exploration, but are not required.

## Setup

1. **Install dependencies:**
   - If you are familiar with pip:
     ```sh
     pip install -r requirements.txt
     ```
   - Or use [UV](https://github.com/astral-sh/uv) (optional, faster):
     ```sh
     uv pip install -r requirements.txt
     ```
   - Or use `pyproject.toml` with Poetry or similar tools.

2. **Set environment variables:**
   - Create a `.env` file with your API keys:
     ```env
     GEMINI_API_KEY=your_gemini_key
     TAVILY_API_KEY=your_tavily_key
     ```

3. **Run FastAPI server:**
   ```sh
   fastapi dev --app server.api:app
   ```

## Features

- Agent graphs with state and memory
- Tool integration for function-calling agents
- FastAPI endpoints for serving responses
- Utilities for graph visualization and tracing

## Example Usage

**Invoke an agent graph:**
```python
from simple.5_agent import graph
result = graph.invoke({"messages": [{"role": "user", "content": "Add 2 and 3"}]})
print(result)
```

**Visualize a graph:**
```python
from simple.utils import print_graph
print_graph(graph, file_name="agent.png")
```

## License

MIT License
