import os
import subprocess

from app.config import JS_DIR, LINKFINDER_PATH, SECRETFINDER_PATH


def run_js_recon(url):
    os.makedirs(JS_DIR, exist_ok=True)

    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")

    linkfinder_output = os.path.join(JS_DIR, f"{safe_name}_linkfinder.html")
    secretfinder_output = os.path.join(JS_DIR, f"{safe_name}_secretfinder.html")

    linkfinder_cmd = [
        "python",
        LINKFINDER_PATH,
        "-i",
        url,
        "-o",
        "html"
    ]

    secretfinder_cmd = [
        "python",
        SECRETFINDER_PATH,
        "-i",
        url,
        "-o",
        "html"
    ]

    linkfinder_result = subprocess.run(linkfinder_cmd, capture_output=True, text=True)
    secretfinder_result = subprocess.run(secretfinder_cmd, capture_output=True, text=True)

    return {
        "url": url,
        "linkfinder_output": linkfinder_output,
        "secretfinder_output": secretfinder_output,
        "linkfinder_stdout": linkfinder_result.stdout,
        "secretfinder_stdout": secretfinder_result.stdout,
    }