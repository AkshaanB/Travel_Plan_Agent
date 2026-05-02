import asyncio
import os
import sys
from typing import List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.tools import Tool

class MCPClient:
    def __init__(self, server_path: Optional[str] = None):
        # Default path to the mcp_server/server.py relative to the backend directory
        if server_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.server_path = os.path.join(base_dir, "mcp_server", "server.py")
        else:
            self.server_path = server_path
            
        self.session: Optional[ClientSession] = None
        self._exit_stack = None

    async def __aenter__(self):
        """Context manager entry to start the MCP server and session."""
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-u", self.server_path],
            env=os.environ.copy()
        )
        
        # Initialize stdio client
        self._client_context = stdio_client(server_params)
        read, write = await self._client_context.__aenter__()
        
        # Initialize session
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit to cleanup the server process."""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if hasattr(self, "_client_context") and self._client_context:
            await self._client_context.__aexit__(exc_type, exc_val, exc_tb)

    async def get_langchain_tools(self) -> List[Tool]:
        """
        Discovers tools from the MCP server and wraps them as LangChain Tool objects.
        """
        if not self.session:
            raise RuntimeError("MCP session not initialized. Use 'async with' context manager.")

        mcp_tools = await self.session.list_tools()
        langchain_tools = []

        for mcp_tool in mcp_tools.tools:
            # Create a closure to capture the tool name for the call
            def make_call(name):
                async def call_mcp_tool(**kwargs):
                    result = await self.session.call_tool(name, kwargs)
                    if result.isError:
                        return f"Error: {result.content}"
                    return result.content[0].text
                return call_mcp_tool

            langchain_tools.append(
                Tool(
                    name=mcp_tool.name,
                    description=mcp_tool.description,
                    func=None, # LangChain will use the coroutine for async execution
                    coroutine=make_call(mcp_tool.name)
                )
            )
            
        return langchain_tools

# Example usage utility
async def fetch_tools():
    async with MCPClient() as client:
        return await client.get_langchain_tools()
