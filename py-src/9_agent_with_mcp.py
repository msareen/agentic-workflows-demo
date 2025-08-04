import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from load_llm import llm

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["py-src/mcp/math_server.py"],  # Absolute path recommended
                "transport": "stdio",
            },
            # "weather": {
            #     "url": "http://localhost:8000/mcp",
            #     "transport": "streamable_http",
            # }
        }
    )

    tools = await client.get_tools()

    agent = create_react_agent(llm, tools)

    math_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]
    })

    print("Math Response:", math_response)

    # Uncomment below if your weather server is running
    # weather_response = await agent.ainvoke({
    #     "messages": [{"role": "user", "content": "what is the weather in nyc?"}]
    # })
    # print("Weather Response:", weather_response)

if __name__ == "__main__":
    asyncio.run(main())
