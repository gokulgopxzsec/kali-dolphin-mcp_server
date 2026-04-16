import os
import subprocess
import tempfile

from app.config import NUCLEI_PATH, NUCLEI_RESULTS_DIR


def run_nuclei_on_hosts(live_hosts):
    os.makedirs(NUCLEI_RESULTS_DIR, exist_ok=True)

    cleaned_hosts = []

    for host in live_hosts:
        if isinstance(host, str):
            clean_host = host.split(" ")[0].strip()
            if clean_host.startswith("http"):
                cleaned_hosts.append(clean_host)

    if not cleaned_hosts:
        return {
            "status": "error",
            "message": "No valid live hosts found",
            "findings": []
        }

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_file.write("\n".join(cleaned_hosts))
        temp_hosts_file = temp_file.name

    output_file = os.path.join(
        NUCLEI_RESULTS_DIR,
        "multi_host_scan.txt"
    )

    command = [
    NUCLEI_PATH,
    "-l",
    temp_hosts_file,
    "-severity",
    "info,low,medium,high,critical",
    "-rate-limit",
    "20",
    "-timeout",
    "10",
    "-retries",
    "2",
    "-c",
    "10",
    "-o",
    output_file
]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=1800
        )

        findings = []

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
                findings = [line.strip() for line in f if line.strip()]

        return {
            "status": "success",
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_file": output_file,
            "total_hosts": len(cleaned_hosts),
            "total_findings": len(findings),
            "findings": findings
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Nuclei scan timed out",
            "findings": []
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "findings": []
        }

    finally:
        if os.path.exists(temp_hosts_file):
            os.remove(temp_hosts_file)