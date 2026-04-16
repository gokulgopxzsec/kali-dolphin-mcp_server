import subprocess


def run_katana(host):
    try:
        result = subprocess.run(
            [
                "katana",
                "-u",
                host,
                "-silent",
                "-jc",
                "-d",
                "3"
            ],
            capture_output=True,
            text=True,
            timeout=300
        )

        urls = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        return {
            "status": "success",
            "urls": urls
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "urls": []
        }