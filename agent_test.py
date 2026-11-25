import asyncio
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

OPENROUTER_API_KEY = ""
GITHUB_PAT = ""

async def main():
    client = MultiServerMCPClient({
        "github": {
            "transport": "http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {
                "Authorization": f"Bearer {GITHUB_PAT}",
                "X-MCP-Toolsets": "repos,issues",
                "X-MCP-Readonly": "true",
            },
        }
    })

    tools = await client.get_tools()
    print(f"Connected! Discovered {len(tools)} tools.")
    print("Type 'exit' or 'quit' to stop.\n")

    model = ChatOpenRouter(
        model="nvidia/nemotron-3.5-lightning:free",
        api_key=OPENROUTER_API_KEY,
        temperature=0,
    )

    # InMemorySaver keeps full conversation + tool-call history in RAM
    agent = create_agent(model, tools, checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "github-chat-1"}}

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        print(f"\nAgent: {response['messages'][-1].content}")

asyncio.run(main())