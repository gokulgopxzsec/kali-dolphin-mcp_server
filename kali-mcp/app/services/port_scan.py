import subprocess


def run_naabu(domain):
    try:
        result = subprocess.run(
            [
                "naabu",
                "-host",
                domain,
                "-top-ports",
                "100"
            ],
            capture_output=True,
            text=True,
            timeout=300
        )

        ports = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        return {
            "status": "success",
            "ports": ports
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "ports": []
        }