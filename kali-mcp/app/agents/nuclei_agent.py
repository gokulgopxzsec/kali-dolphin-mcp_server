import os
import subprocess

from app.config import NUCLEI_PATH


def run_nuclei(target):
    os.makedirs("nuclei_results", exist_ok=True)

    safe_target = (
        target.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(".", "_")
    )

    output_file = os.path.abspath(
        f"nuclei_results/{safe_target}.txt"
    )

    command = [
        NUCLEI_PATH,
        "-u",
        target,
        "-severity",
        "info,low,medium,high,critical",
        "-o",
        output_file
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        findings = []

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
                findings = f.read().splitlines()

        return {
            "status": "success" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_file": output_file,
            "total_findings": len(findings),
            "findings": findings[:100]
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "output_file": output_file
        }