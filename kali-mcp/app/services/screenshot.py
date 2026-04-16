import os
import subprocess

from app.config import SCREENSHOT_DIR


def take_screenshots(hosts):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    hosts_file = os.path.join(SCREENSHOT_DIR, "hosts.txt")

    with open(hosts_file, "w", encoding="utf-8") as f:
        for host in hosts:
            clean_host = host.split(" ")[0].strip()
            f.write(f"{clean_host}\n")

    try:
        subprocess.run(
            [
                "gowitness",
                "file",
                "-f",
                hosts_file,
                "--screenshot-path",
                SCREENSHOT_DIR
            ],
            capture_output=True,
            text=True,
            timeout=300
        )
    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")

    return SCREENSHOT_DIR