import os
import subprocess
from app.config import PYTHON_PATH, LINKFINDER_PATH, SECRETFINDER_PATH, JS_RESULTS_DIR


def analyze_js(js_url, output_prefix):
    os.makedirs(JS_RESULTS_DIR, exist_ok=True)

    linkfinder_output = os.path.join(JS_RESULTS_DIR, f"{output_prefix}_linkfinder.txt")
    secretfinder_output = os.path.join(JS_RESULTS_DIR, f"{output_prefix}_secretfinder.txt")

    subprocess.run([
        PYTHON_PATH,
        LINKFINDER_PATH,
        "-i", js_url,
        "-o", "cli"
    ], capture_output=True, text=True)

    subprocess.run([
        PYTHON_PATH,
        SECRETFINDER_PATH,
        "-i", js_url,
        "-o", "cli"
    ], capture_output=True, text=True)

    return {
        "linkfinder_output": linkfinder_output,
        "secretfinder_output": secretfinder_output
    }