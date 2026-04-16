SUBFINDER_PATH = r"C:\Users\gokul\go\bin\subfinder.exe"
HTTPX_PATH = r"C:\Users\gokul\go\bin\httpx.exe"
NUCLEI_PATH = r"C:\Users\gokul\go\bin\nuclei.exe"
WAYBACKURLS_PATH = r"C:\Users\gokul\go\bin\waybackurls.exe"
FFUF_PATH = r"C:\ffuf\ffuf.exe"
GAU_PATH = r"C:\Users\gokul\go\bin\gau.exe"
KATANA_PATH = r"C:\Users\gokul\go\bin\katana.exe"
GOWITNESS_PATH = r"C:\gowitness\gowitness.exe"
LINKFINDER_PATH = r"C:\tools\LinkFinder\linkfinder.py"
SECRETFINDER_PATH = r"C:\tools\SecretFinder\SecretFinder.py"
PYTHON_PATH = r"C:\Python311\python.exe"

SCREENSHOT_DIR = "reports/screenshots"
NUCLEI_PATH = r"C:\Users\gokul\go\bin\nuclei.exe"
NUCLEI_RESULTS_DIR = "app/nuclei_results"
NUCLEI_RESULTS_DIR = "nuclei_results"
FFUF_RESULTS_DIR = "ffuf_results"
JS_RESULTS_DIR = "js_results"
REPORTS_DIR = "app/reports"
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "dolphin-llama3:8b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")