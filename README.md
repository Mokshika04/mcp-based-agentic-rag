# MCP-based Agentic RAG (Retrieval-Augmented Generation)

## Overview

This project implements a simple tool-augmented conversational agent using:

- `fastmcp` for building an MCP tool server
- `langchain` agents with Ollama LLM (`llama3.2:latest`) on the client side
- Local RAG search over documents via a vector store + similarity search
- Specialty connectors for arXiv, GitHub and news data

Primary modules:

- `server.py`: MCP server exposes tools:
  - `search_papers` (from `tools/arxiv_tool.py`)
  - `search_repo_by_topic` (from `tools/github_tool.py`)
  - `fetch_latest_news` (from `tools/newsdata_tool.py`)
  - `search_local_documents` (from `local_rag_pipeline/vector_search.py`)

- `client.py`: interactive agent loop; uses LangChain `create_tool_calling_agent` + `ChatOllama`.
- `local_rag_pipeline/vector_search.py`: local document embedding + retrieval API.
- `local_rag_pipeline/vector_store.py`: store / index helper for local RAG data.

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

- `research_tool` → arXiv search
- `github_tool` → repository search by topic
- `news_tool` → latest news search
- `rag_tool` → local documents search

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
- `tools/arxiv_tool.py` - arXiv search wrapper
- `tools/github_tool.py` - GitHub search wrapper
- `tools/newsdata_tool.py` - News search wrapper
- `local_rag_pipeline/vector_search.py` - RAG query logic
- `local_rag_pipeline/vector_store.py` - Persistence and indexes

