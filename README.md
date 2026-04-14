# MCP-based Agentic RAG (Retrieval-Augmented Generation)

## Overview

This project implements a simple tool-augmented conversational agent using:

- `fastmcp` for building an MCP tool server
- `langchain` agents with Ollama LLM (`llama3.2:latest`) on the client side
- Local RAG search over documents via a vector store + similarity search
- Specialty connectors for arXiv, GitHub, news data, and web search

Primary modules:

- `server.py`: MCP server exposes tools:
  - `agent_fetch_tools` (from `worker_agents/technical_agent.py`): Multi-tool orchestrator for research and search tools.
  - `conversational_agent` (from `worker_agents/general_agent.py`): General-purpose conversational handler.

- `client.py`: Interactive agent loop; uses LangChain `create_tool_calling_agent` + `ChatOllama`. **Includes a main orchestrator that dynamically selects which agent to call (e.g., `agent_fetch_tools` or `conversational_agent`) based on the user's query.**
- `local_rag_pipeline/vector_search.py`: Local document embedding + retrieval API.
- `local_rag_pipeline/vector_store.py`: Store / index helper for local RAG data.

## Features

- Agent can call external tools through MCP service.
- Local RAG pipeline supports semantic search over local documents stored in `MCP pdf data`, `qdrant_data`, etc.
- Easy extension by adding tool functions and registering with FastMCP.

## Prerequisites

- Python 3.10+
- Ollama installed and model `llama3.2:latest` available.
- virtualenv/uv (optional but recommended)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
uv install -r requirements.txt
```

## Startup

1. Run MCP server:

```bash
uv run server.py
```

2. In another terminal, run client:

```bash
uv run client.py
```

3. Type queries. Tools are:

- `agent_fetch_tools` → Multi-tool orchestrator for research and search tools.
- `conversational_agent` → General-purpose conversational handler.

Type `exit`, `bye`, `quit` to quit.

## Customization

- Add new tools in `tools/*.py` and register in `server.py`.
- Update local RAG processing in `local_rag_pipeline/vector_search.py`.
- Modify prompt in `client.py` under `ChatPromptTemplate`.

## Troubleshooting

- `Ollama` connectivity: check model installed and daemon running.
- `FastMCP` endpoint is `http://127.0.0.1:8000/sse`.
- Ensure local RAG vectors exist and path configured correctly.

## Project files

- `client.py` - User-facing async agent loop
- `server.py` - MCP tool server
- `worker_agents/technical_agent.py` - Multi-tool orchestrator
- `worker_agents/general_agent.py` - General-purpose conversational handler
- `tools/arxiv_tool.py` - arXiv search wrapper
- `tools/github_tool.py` - GitHub search wrapper
- `tools/newsdata_tool.py` - News search wrapper
- `tools/web_search_tool.py` - Web search wrapper
- `local_rag_pipeline/vector_search.py` - RAG query logic
- `local_rag_pipeline/vector_store.py` - Persistence and indexes

