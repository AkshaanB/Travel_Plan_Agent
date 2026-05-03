from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from mcp_client.client import MCPClient
import logging
import os

# Setup Logging
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize and start MCP Client
    logger.info("Starting MCP Server...")
    mcp_client = MCPClient()
    await mcp_client.__aenter__()
    app.state.mcp_client = mcp_client
    
    # Pre-fetch tools to ensure connection is working
    try:
        app.state.tools = await mcp_client.get_langchain_tools()
        logger.info(f"MCP Server connected. {len(app.state.tools)} tools loaded.")
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        app.state.tools = []

    yield
    
    # Shutdown: Cleanup MCP Client
    logger.info("Shutting down MCP Server...")
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

from graph.workflow import app_graph
from langchain_core.messages import HumanMessage
from utils.guardrails import check_input_guardrails, check_output_guardrails

class ChatRequest(BaseModel):
    text: str

@app.get("/")
async def index():
    return {"message": "Welcome to the Travel Planning Agent"}

@app.get("/health")
async def health_check():
    return {"status": "The application is running..."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, fastapi_req: Request):
    logger.info(f"Received chat request: {request.text}")
    
    # 1. Input Guardrail
    input_check = check_input_guardrails(request.text)
    if not input_check["is_valid"]:
        logger.warning(f"Request blocked by guardrails. Reason: {input_check['reason']}")
        return {
            "status": "blocked",
            "reason": input_check["reason"],
            "message": "Your request was blocked by the safety system."
        }

    # 2. Process with LangGraph Orchestrator
    # Note: fastapi_req.app.state.tools is populated during startup by lifespan
    tools = getattr(fastapi_req.app.state, "tools", [])
    state = {
        "messages": [HumanMessage(content=request.text)],
        "tools": tools
    }
    
    logger.info("Invoking LangGraph orchestrator...")
    final_state = await app_graph.ainvoke(state)
    
    # 3. Extract Response
    # The last message in the state is the response from the agent
    response_msg = final_state["messages"][-1]
    response_text = response_msg.content
    classified_intent = final_state.get("intent", "unknown")
    
    # 4. Output Guardrail
    output_check = check_output_guardrails(response_text)
    if not output_check["is_valid"]:
        logger.warning(f"Response blocked by guardrails. Reason: {output_check['reason']}")
        return {
            "status": "blocked",
            "reason": output_check["reason"],
            "message": "The generated response was blocked for safety reasons."
        }

    logger.info(f"Request processed successfully. Classified intent: {classified_intent}")
    return {
        "status": "success",
        "user_query": request.text,
        "classified_intent": classified_intent,
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
