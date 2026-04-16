# Kali MCP Research Server

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

## Run

```bash
uvicorn app.server:app --reload
```

## Ingest Knowledge Base

```bash
python app/rag/ingest.py
```

## Docker

```bash
docker compose up --build
```

