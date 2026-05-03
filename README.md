# ✈️ Travel Planning Agent Chatbot

A powerful, multi-agent AI travel assistant built with **FastAPI**, **LangGraph**, and **React**. This project utilizes **Ollama** for local LLM inference and follows the **Model Context Protocol (MCP)** for extensible tool integration.

## 🚀 Key Features

- **Multi-Agent Orchestration**: Uses `LangGraph` to route user queries between specialized agents (Travel Planner, Recommender, and QA).
- **Local Intelligence**: Powered by `llama3.2:3b` via **Ollama** for fast, private, and local processing.
- **Intent Classification**: Automatically identifies if a user wants to plan a trip, get recommendations, or ask general travel questions.
- **MCP Tool Integration**: A standalone MCP server providing mock tools for real-time (simulated) flight, hotel, and activity data.
- **Hybrid Guardrails**: A two-tier safety system combining rule-based Regex and LLM-based auditing to prevent prompt injection and keep the agent on-topic.
- **Premium Frontend**: A modern, responsive React + Vite interface with rich aesthetics and smooth micro-animations.

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
│   ├── mcp/                # MCP Client implementation
│   ├── mcp_server/         # Standalone MCP Tool Server (Mock APIs)
│   ├── utils/              # Guardrails and helpers
│   └── main.py             # API Entry point
├── frontend/               # React Vite Application
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

### 2. Setup the MCP Server
The MCP server provides the tools for the agent to "call".
```powershell
cd backend/mcp_server
pip install -r requirements.txt
python server.py
```

### 3. Setup the Backend API
```powershell
cd backend
pip install -r requirements.txt
python main.py
```
The API will be available at `http://localhost:8000`.

### 4. Setup the Frontend
```powershell
cd frontend
npm install
npm run dev
```

---

## 🛡️ Guardrails in Action
The agent is protected against:
- **Prompt Injection**: "Ignore previous instructions..."
- **Off-topic Queries**: "How do I write a Python script?" (Filtered to stay on travel)
- **Sensitive Data Leakage**: Credit cards, API keys, etc.

---

## 🧪 Testing the API
You can test the multi-agent intent classification using `curl` or PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/chat" -ContentType "application/json" -Body '{"text": "Plan a 3-day trip to Tokyo"}'
```

---
*Created by Antigravity AI Assistant.*
