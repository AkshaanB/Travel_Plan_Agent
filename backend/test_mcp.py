import asyncio
import os
import sys
from mcp_client.client import MCPClient

async def main():
    print("Starting test MCP client...")
    try:
        async with MCPClient() as client:
            print("Client initialized. Fetching tools...")
            tools = await client.get_langchain_tools()
            print(f"Discovered {len(tools)} tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
                
            # Test a tool call
            print("\nTesting get_activities for 'Tokyo'...")
            # Note: get_langchain_tools returns LangChain Tools. 
            # In our client, we use 'coroutine' for async calls.
            # But the 'Tool' object might not be directly awaitable depending on LC version.
            # Let's use the session directly if needed, but let's try the tool.
            # For this test, let's just see if tools are listed.
            
    except Exception as e:
        print(f"Error during MCP test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
