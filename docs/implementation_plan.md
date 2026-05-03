# Travel Planning Agent Chatbot - Implementation Plan

This document outlines the architecture and implementation strategy for building a multi-agent Travel Planning Chatbot. The system utilizes a React (Vite) frontend, a FastAPI backend using LangGraph, an Ollama-hosted `llama3.2:3b` LLM, and a standalone Model Context Protocol (MCP) server for tool integrations.

## Goal Description
Develop a robust, locally-hosted Travel Planning Agent capable of understanding user intents, answering general queries, recommending destinations, and planning detailed itineraries using mocked tools via MCP. The application emphasizes a premium frontend experience and a scalable, secure agentic backend managed by LangGraph.

> [!NOTE]
> The system leverages `llama3.2:3b` via Ollama to ensure fast, local execution while maintaining the ability to process tool calls and classify intents.

## User Review Required
The implementation plan has been updated with your preferences. Please review the updated architecture and component structure. Once approved, we will proceed to execution.

> [!IMPORTANT]  
> The frontend will be designed with a premium, dynamic aesthetic (e.g., modern typography, smooth animations, glassmorphism) using vanilla CSS per best practices, avoiding generic styling.

## Proposed Architecture

### 1. Model Layer (Ollama)
- **Model**: `llama3.2:3b`
- **Purpose**: Acts as the core reasoning engine for intent classification, tool invocation, and natural language generation.

### 2. Backend Layer (FastAPI & LangGraph)
The backend will manage the API endpoints and the LangGraph multi-agent orchestrator.

- **`/chat` Endpoint**: Receives user messages and returns agent responses.
- **Guardrails (Custom)**:
  - **Input Guardrails**: Lightweight custom functions to pre-check user input for prompt injection or off-topic queries before they hit the LLM.
  - **Output Guardrails**: Validates the LLM's response format and checks for hallucinated or inappropriate content.
- **LangGraph Orchestrator**:
  - Manages conversation state and memory.
  - **Classifier Node**: Routes the query based on intent (`travel_plan`, `general_qa`, `travel_recommend`).
  - **Agent Nodes**: Specific nodes for handling the routed intents.

### 3. Tool Layer (Standalone MCP Server)
- **Architecture**: A completely separate standard MCP server process that the FastAPI backend communicates with via an MCP Client.
- **Tools**:
  - `get_mock_flights(origin, destination, dates)`
  - `get_mock_hotels(location, dates)`
  - `get_mock_activities(location)`
- These tools will return structured mock JSON data to simulate API latency and responses.

### 4. Frontend Layer (React + Vite)
- **Framework**: React via Vite.
- **Styling**: Vanilla CSS with a focus on rich aesthetics, modern colors (e.g., sleek dark mode), and micro-animations for message bubbles and loading states.
- **Components**:
  - `ChatbotLayout`: Main container.
  - `MessageThread`: Displays user and agent messages.
  - `MessageInput`: Text area with a dynamic send button.
  - `ThinkingIndicator`: Visual feedback when the orchestrator is processing or calling tools.

## Proposed Changes

---

### Backend (`backend/`)
#### [NEW] `backend/main.py`
Entry point for FastAPI, defining CORS and the primary `/chat` REST endpoint.

#### [NEW] `backend/graph/workflow.py`
The LangGraph definition, setting up the state, nodes, and conditional edges.

#### [NEW] `backend/graph/nodes.py`
Implementation of the LangGraph nodes: `classifier_node`, `travel_plan_node`, `recommend_node`, `qa_node`.

#### [NEW] `backend/mcp/client.py`
MCP Client implementation to connect to the standalone MCP server and execute tools.

#### [NEW] `backend/utils/guardrails.py`
Custom lightweight Python functions for input and output validation.

#### [NEW] `backend/requirements.txt`
Dependencies including `fastapi`, `uvicorn`, `langgraph`, `langchain-ollama`, etc.

---

### MCP Server (`mcp_server/`)
#### [NEW] `mcp_server/server.py`
Standalone MCP server implementation exposing the mock travel tools using the official Python MCP SDK.

#### [NEW] `mcp_server/requirements.txt`
Dependencies for the MCP server (`mcp`).

---

### Frontend (`frontend/`)
#### [NEW] `frontend/package.json` & setup
Vite setup configuration.

#### [NEW] `frontend/src/App.jsx`
Main application component.

#### [NEW] `frontend/src/index.css`
Core design system, CSS variables for premium aesthetics, animations.

#### [NEW] `frontend/src/components/Chat/...`
Various UI components for the chat interface.

## Verification Plan

### Automated Tests
- Unit tests for the custom guardrails to ensure off-topic or malicious prompts are blocked.
- Unit tests for the LangGraph routing logic.

### Manual Verification
1. Start the Ollama server (`llama3.2:3b`).
2. Start the standalone MCP server.
3. Start the FastAPI backend.
4. Run the React frontend.
5. Verify guardrails block off-topic queries.
6. Verify LangGraph correctly routes a general question to the QA node.
7. Verify LangGraph routes a planning request to the Planner node, which successfully calls tools on the separate MCP server and returns a cohesive itinerary.
