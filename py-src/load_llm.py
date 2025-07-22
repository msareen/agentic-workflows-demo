from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")


llm = init_chat_model("google_genai:gemini-2.5-flash")

# llm.bind_tools
# llm.with_structured_output()

__all__ = [llm]