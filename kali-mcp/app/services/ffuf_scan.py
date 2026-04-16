import subprocess
import json


def should_fuzz(host):
    return host.startswith("http")


def run_ffuf(host, wordlist):
    try:
        command = [
            "ffuf",
            "-u",
            f"{host}/FUZZ",
            "-w",
            wordlist,
            "-mc",
            "200,204,301,302,307,401,403",
            "-rate",
            "50",
            "-timeout",
            "10",
            "-of",
            "json",
            "-o",
            "ffuf_output.json"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300
        )

        findings = []

        try:
            with open("ffuf_output.json", "r", encoding="utf-8") as f:
                data = json.load(f)

                for item in data.get("results", []):
                    findings.append({
                        "url": item.get("url"),
                        "status": item.get("status"),
                        "length": item.get("length")
                    })
        except Exception:
            pass

        return {
            "status": "success",
            "command": command,
            "findings": findings,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "findings": []
        }