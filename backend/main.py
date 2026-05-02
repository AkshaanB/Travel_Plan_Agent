from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from mcp_client.client import MCPClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize and start MCP Client
    print("Starting MCP Server...", flush=True)
    mcp_client = MCPClient()
    await mcp_client.__aenter__()
    app.state.mcp_client = mcp_client
    
    # Pre-fetch tools to ensure connection is working
    try:
        app.state.tools = await mcp_client.get_langchain_tools()
        print(f"MCP Server connected. {len(app.state.tools)} tools loaded.", flush=True)
    except Exception as e:
        print(f"Failed to load MCP tools: {e}", flush=True)
        app.state.tools = []

    yield
    
    # Shutdown: Cleanup MCP Client
    print("Shutting down MCP Server...", flush=True)
    await mcp_client.__aexit__(None, None, None)

app = FastAPI(
    title="Travel Planning Agent API", 
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from graph.nodes import classifier_node
from langchain_core.messages import HumanMessage
from utils.guardrails import check_input_guardrails, check_output_guardrails

class ChatRequest(BaseModel):
    text: str

@app.get("/")
async def index():
    return {"message": "Welcome to the Travel Planning Agent"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. Input Guardrail
    input_check = check_input_guardrails(request.text)
    if not input_check["is_valid"]:
        return {
            "status": "blocked",
            "reason": input_check["reason"],
            "message": "Your request was blocked by the safety system."
        }

    # 2. Process with Classifier (Placeholder for LangGraph)
    state = {"messages": [HumanMessage(content=request.text)]}
    result = classifier_node(state)
    
    # 3. Dummy response for now (until agents are fully implemented)
    response_text = f"Identified intent: {result['intent']}. I am ready to help you with your travel needs!"
    
    # 4. Output Guardrail
    output_check = check_output_guardrails(response_text)
    if not output_check["is_valid"]:
        return {
            "status": "blocked",
            "reason": output_check["reason"],
            "message": "The generated response was blocked for safety reasons."
        }

    return {
        "status": "success",
        "user_query": request.text,
        "classified_intent": result["intent"],
        "response": response_text
    }

@app.get("/mcp/status")
async def mcp_status(request: Request):
    """Check the status of the MCP server and list available tools."""
    tools = getattr(request.app.state, "tools", [])
    return {
        "mcp_connected": hasattr(request.app.state, "mcp_client"),
        "tools_loaded": len(tools),
        "tools": [t.name for t in tools]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
