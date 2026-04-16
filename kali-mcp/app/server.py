from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.recon_agent import run_recon
from app.agents.nuclei_agent import run_nuclei
from app.agents.rag_agent import search_knowledge_base
from app.agents.report_agent import generate_report

app = FastAPI(title="Kali MCP Research Server")


@app.get("/")
def root():
    return {"message": "Kali MCP Server Running"}


class ReconRequest(BaseModel):
    target: str
    prompt: str | None = None


@app.post("/recon")
def recon(request: ReconRequest):
    return run_recon(request.target, request.prompt)

@app.post("/scan")
def scan_target(target: str):
    recon_results = run_recon(target)
    nuclei_results = run_nuclei(target)
    rag_results = search_knowledge_base(str(nuclei_results))
    report_path = generate_report(
        target,
        recon_results,
        nuclei_results,
        rag_results
    )

    return {
        "target": target,
        "recon": recon_results,
        "nuclei": nuclei_results,
        "rag": rag_results,
        "report": report_path
    }