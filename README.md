# AI Graph Search

A Streamlit app that indexes directories into a Neo4j knowledge graph and lets you search them with natural language queries powered by an LLM agent.

## How it works

- **Index**: Point the app at a directory. It scans the files, generates descriptions (including image descriptions), and stores them as nodes and relationships in Neo4j.
- **Search**: Ask a natural language question. An LLM agent translates it into Cypher queries and returns the most relevant results.

Two Griptape Nodes workflows run as background FastAPI servers:
- `create_graph` on port 8005 — indexing workflow
- `retrieve_from_graph` on port 8006 — search workflow

## Requirements

- Python 3.12
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A running Neo4j instance

## Setup

```bash
bash start.sh
```

That's it. `start.sh` runs `uv sync` to install dependencies, then launches the Streamlit app. The workflow servers start automatically in the background when the app loads.

## Project structure

```
app.py                          # Streamlit UI
workflow_server.py              # FastAPI server that runs a single workflow
workflow_server_manager.py      # Spawns and manages the workflow server subprocesses
workflows/
  create_graph.py               # Indexing workflow (Griptape Nodes generated)
  retrieve_from_graph.py        # Search workflow (Griptape Nodes generated)
griptape-nodes/                 # Local modified griptape-nodes engine
griptape-nodes-library-standard/  # Custom standard node library
griptape-nodes-library-neo4j/   # Neo4j integration node library
```

## Ports

| Service | Port |
|---------|------|
| Streamlit | 8501 (default) |
| Indexing workflow server | 8005 |
| Search workflow server | 8006 |

Make sure ports 8005 and 8006 are free before starting.
