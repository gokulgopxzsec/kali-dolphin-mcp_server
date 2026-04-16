import os
from pathlib import Path

BASE_DIR = Path("kali-mcp")

folders = [
    "app",
    "app/agents",
    "app/tools",
    "app/rag",
    "app/rag/chroma_db",
    "app/reports",
    "data",
    "screenshots",
    "logs",
    "nuclei_results",
    "notes",
]

files = {
    "requirements.txt": """fastapi
uvicorn
langchain
langchain-community
chromadb
faiss-cpu
ollama
pydantic
sqlalchemy
playwright
beautifulsoup4
httpx
rich
typer
python-multipart
jinja2
markdown
redis
celery
python-dotenv
""",

    "docker-compose.yml": """version: '3.9'

services:
  fastapi-app:
    build: .
    container_name: kali-mcp-api
    ports:
      - '8000:8000'
    volumes:
      - ./:/app
    depends_on:
      - chromadb
      - redis
      - postgres

  chromadb:
    image: chromadb/chroma
    container_name: chromadb
    ports:
      - '8001:8000'

  redis:
    image: redis:alpine
    container_name: redis
    ports:
      - '6379:6379'

  postgres:
    image: postgres:15
    container_name: postgres
    environment:
      POSTGRES_USER: kali
      POSTGRES_PASSWORD: kali
      POSTGRES_DB: kali_mcp
    ports:
      - '5432:5432'
""",

    "app/server.py": """from fastapi import FastAPI
from app.agents.recon_agent import run_recon
from app.agents.nuclei_agent import run_nuclei
from app.agents.rag_agent import search_knowledge_base
from app.agents.report_agent import generate_report

app = FastAPI(title='Kali MCP Research Server')

@app.get('/')
def root():
    return {'message': 'Kali MCP Server Running'}

@app.post('/scan')
def scan_target(target: str):
    recon_results = run_recon(target)
    nuclei_results = run_nuclei(target)
    rag_results = search_knowledge_base(str(nuclei_results))
    report_path = generate_report(target, recon_results, nuclei_results, rag_results)

    return {
        'target': target,
        'recon': recon_results,
        'nuclei': nuclei_results,
        'rag': rag_results,
        'report': report_path
    }
""",

    "app/agents/recon_agent.py": """from app.tools.subfinder import run_subfinder
from app.tools.httpx_tool import run_httpx
from app.tools.wayback import run_wayback


def run_recon(target):
    subdomains = run_subfinder(target)
    live_hosts = run_httpx(subdomains)
    urls = run_wayback(target)

    return {
        'subdomains': subdomains,
        'live_hosts': live_hosts,
        'urls': urls
    }
""",

    "app/agents/nuclei_agent.py": """import subprocess


def run_nuclei(target):
    safe_target = target.replace('.', '_').replace('/', '_')
    output_file = f'nuclei_results/{safe_target}.txt'

    command = [
        'nuclei',
        '-u',
        target,
        '-severity',
        'low,medium,high,critical',
        '-o',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        return {
            'status': 'success',
            'output_file': output_file
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }
""",

    "app/agents/rag_agent.py": """import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path='app/rag/chroma_db')
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')

collection = client.get_or_create_collection(
    name='security_knowledge',
    embedding_function=embedding_fn
)


def search_knowledge_base(query):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results
""",

    "app/agents/report_agent.py": """from datetime import datetime


def generate_report(target, recon_results, nuclei_results, rag_results):
    safe_target = target.replace('.', '_').replace('/', '_')
    report_path = f'app/reports/{safe_target}_report.md'

    content = f'''# Security Report for {target}

Generated: {datetime.now()}

## Recon Results
{recon_results}

## Nuclei Results
{nuclei_results}

## RAG Correlation
{rag_results}
'''

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return report_path
""",

    "app/tools/subfinder.py": """import subprocess


def run_subfinder(domain):
    try:
        result = subprocess.check_output([
            'subfinder',
            '-d',
            domain,
            '-silent'
        ])
        return result.decode().splitlines()
    except Exception as e:
        return [f'Error: {e}']
""",

    "app/tools/httpx_tool.py": """import subprocess
import tempfile


def run_httpx(subdomains):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write('\n'.join(subdomains))
        tmp.flush()

        try:
            result = subprocess.check_output([
                'httpx',
                '-l',
                tmp.name,
                '-silent'
            ])
            return result.decode().splitlines()
        except Exception as e:
            return [f'Error: {e}']
""",

    "app/tools/wayback.py": """import subprocess


def run_wayback(domain):
    try:
        result = subprocess.check_output([
            'waybackurls',
            domain
        ])
        return result.decode().splitlines()
    except Exception as e:
        return [f'Error: {e}']
""",

    "app/rag/ingest.py": """import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path='app/rag/chroma_db')
collection = client.get_or_create_collection(name='security_knowledge')

DATA_DIR = Path('data')

for file in DATA_DIR.glob('*.txt'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    collection.add(
        documents=[content],
        ids=[file.stem],
        metadatas=[{'source': str(file)}]
    )

print('Knowledge base ingestion complete.')
""",

    "app/rag/embeddings.py": """import ollama


def generate_embedding(text):
    response = ollama.embeddings(
        model='nomic-embed-text',
        prompt=text
    )
    return response['embedding']
""",

    ".env": """OLLAMA_HOST=http://host.docker.internal:11434
DEFAULT_MODEL=qwen3.5:9b
EMBED_MODEL=nomic-embed-text
""",

    "README.md": """# Kali MCP Research Server

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

"""
}

def create_project():
    BASE_DIR.mkdir(exist_ok=True)
 
for folder in folders:
    path = BASE_DIR / folder
    path.mkdir(parents=True, exist_ok=True)

    init_file = path / '__init__.py'
    if 'app' in str(path) and not init_file.exists():
        init_file.write_text('')

for file_path, content in files.items():
    full_path = BASE_DIR / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding='utf-8')

print('Kali MCP project scaffold created successfully.')


if __name__ == '__main___':
    create_project()

# ````

# ## Run the Generator

# ```bash
# python generate_kali_mcp.py
# ````

# ## Then Install Core Recon Tools

# ```bash
# sudo apt update
# sudo apt install golang-go -y

# GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
# GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
# GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
# GO111MODULE=on go install -v github.com/tomnomnom/waybackurls@latest
# ```

# ## Start the API

# ```bash
# uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
# ```

# ## Example API Request

# ```bash
# curl -X POST "http://127.0.0.1:8000/scan?target=example.com"
# ```

# This gives you a complete starter scaffold with:

# * FastAPI server
# * Recon agent
# * Nuclei wrapper
# * Chroma RAG
# * Markdown report generation
# * Docker compose
# * Environment variables
# * Knowledge ingestion pipeline
# * Recon tool wrappers
# * Organized project structure
