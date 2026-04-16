import subprocess
import tempfile
import os
from app.config import HTTPX_PATH


def probe_hosts(subdomains):
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as f:
        for sub in subdomains:
            f.write(sub + "\n")
        input_file = f.name

    output_file = input_file + "_live.txt"

    cmd = [
        HTTPX_PATH,
        "-l", input_file,
        "-title",
        "-tech-detect",
        "-status-code",
        "-follow-redirects",
        "-silent",
        "-o", output_file
    ]

    subprocess.run(cmd, capture_output=True, text=True)

    live_hosts = []

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            live_hosts = [line.strip() for line in f if line.strip()]

    return live_hosts