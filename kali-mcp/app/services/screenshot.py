import os
import subprocess

from app.config import SCREENSHOT_DIR


def take_screenshots(hosts, domain):
    output_dir = os.path.join(SCREENSHOT_DIR, domain)
    os.makedirs(output_dir, exist_ok=True)

    hosts_file = os.path.join(output_dir, "hosts.txt")

    with open(hosts_file, "w", encoding="utf-8") as f:
        for host in hosts:
            f.write(f"{host}\n")

    try:
        subprocess.run(
            [
                "gowitness",
                "file",
                "-f",
                hosts_file,
                "--screenshot-path",
                output_dir
            ],
            capture_output=True,
            text=True,
            timeout=300
        )
    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")

    return output_dir