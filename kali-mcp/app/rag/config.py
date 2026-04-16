import os

HTTPX_PATH = r"C:\Users\gokul\go\bin\httpx.exe"
SUBFINDER_PATH = r"C:\Users\gokul\go\bin\subfinder.exe"
NUCLEI_PATH = r"C:\Users\gokul\go\bin\nuclei.exe"
WAYBACKURLS_PATH = r"C:\Users\gokul\go\bin\waybackurls.exe"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://172.31.32.1:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen3.5:9b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")