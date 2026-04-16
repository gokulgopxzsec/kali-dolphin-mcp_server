import subprocess
import os
from app.config import FFUF_PATH, FFUF_RESULTS_DIR

HIGH_RISK_WORDS = [
    "admin",
    "api",
    "dev",
    "stage",
    "dashboard",
    "internal"
]


def should_fuzz(host):
    host_lower = host.lower()
    return any(word in host_lower for word in HIGH_RISK_WORDS)


def run_ffuf(host):
    os.makedirs(FFUF_RESULTS_DIR, exist_ok=True)

    safe_name = host.replace("https://", "").replace("http://", "").replace("/", "_")
    output_file = os.path.join(FFUF_RESULTS_DIR, f"{safe_name}.json")

    cmd = [
        FFUF_PATH,
        "-u", f"{host}/FUZZ",
        "-w", "wordlists/common.txt",
        "-mc", "200,204,301,302,307,401,403",
        "-of", "json",
        "-o", output_file
    ]

    subprocess.run(cmd, capture_output=True, text=True)

    return output_file