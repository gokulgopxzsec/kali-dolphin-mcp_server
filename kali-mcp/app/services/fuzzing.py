import os
import subprocess

from app.config import FFUF_PATH, FUZZ_DIR


COMMON_WORDLIST = r"C:\wordlists\common.txt"


def fuzz_url(url):
    os.makedirs(FUZZ_DIR, exist_ok=True)

    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    output_file = os.path.join(FUZZ_DIR, f"{safe_name}.json")

    command = [
        FFUF_PATH,
        "-u",
        f"{url}/FUZZ",
        "-w",
        COMMON_WORDLIST,
        "-mc",
        "200,204,301,302,307,401,403",
        "-o",
        output_file,
        "-of",
        "json"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    return {
        "url": url,
        "return_code": result.returncode,
        "output_file": output_file,
        "stdout": result.stdout,
        "stderr": result.stderr
    }