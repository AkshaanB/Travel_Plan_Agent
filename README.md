# ✈️ Travel Planning Agent Chatbot

A powerful, multi-agent AI travel assistant built with **FastAPI**, **LangGraph**, and **React**. This project utilizes **Ollama** for local LLM inference and follows the **Model Context Protocol (MCP)** for extensible tool integration.

## 🚀 Key Features

- **Multi-Agent Orchestration**: Uses `LangGraph` to route user queries between specialized agents (Travel Planner, Recommender, and QA).
- **Local Intelligence**: Powered by `llama3.2:3b` via **Ollama** for fast, private, and local processing.
- **MCP Tool Integration**: A standalone MCP server providing mock tools for real-time (simulated) flight, hotel, and activity data.
- **Robust Logging**: Comprehensive system logging saved to `logs/app.log` for debugging and auditing.
- **Hybrid Guardrails**: A two-tier safety system combining rule-based Regex and LLM-based auditing to keep the agent on-topic.
- **Minimal MVP Frontend**: A clean, straightforward React + Vite interface focused on core chat functionality.

---

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Vanilla CSS.
- **Backend**: FastAPI, LangGraph, LangChain.
- **LLM Engine**: Ollama (Model: `llama3.2:3b`).
- **Tool Protocol**: Model Context Protocol (MCP).

---

## 📁 Project Structure

```text
Travel_Plan_Agent/
├── backend/                # FastAPI Application
│   ├── graph/              # LangGraph nodes and workflow
│   ├── mcp_client/         # MCP Client implementation
│   ├── mcp_server/         # Standalone MCP Tool Server (Mock APIs)
│   ├── utils/              # Guardrails and helpers
│   └── main.py             # API Entry point
├── frontend/               # React Vite Application
│   ├── src/
│   │   ├── Chat.jsx        # Core Chat Component
│   │   └── index.css       # Minimal MVP Styles
├── logs/                   # System-wide logs
│   └── app.log             # Application log file
├── docs/                   # Implementation plans and documentation
└── README.md
```

---

## ⚙️ Getting Started

### 1. Prerequisites
- **Ollama**: [Download and Install Ollama](https://ollama.com/).
- **Model**: Pull the required model:
  ```powershell
  ollama pull llama3.2:3b
  ```

### 2. Setup and Run the Backend
The backend manages the AI orchestration and connects to the MCP tools.
```powershell
cd backend
# Recommended: Create a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the API server on port 8001
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
The API will be available at `http://localhost:8001`.

### 3. Setup and Run the Frontend
The frontend provides the chat interface.
```powershell
cd frontend
npm install
npm run dev
```
The frontend will typically be available at `http://localhost:5173`. It is pre-configured to communicate with the backend on port 8001.

---

## 🛡️ Guardrails in Action
The agent is protected against:
- **Prompt Injection**: "Ignore previous instructions..."
- **Off-topic Queries**: Filters out non-travel related topics.
- **Sensitive Data Leakage**: Prevents accidental disclosure of private information.

---

## 🧪 Testing the API
You can test the chat endpoint using PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8001/chat" -ContentType "application/json" -Body '{"text": "Plan a 3-day trip to Tokyo"}'
```

---
*Created by Antigravity AI Assistant.*
