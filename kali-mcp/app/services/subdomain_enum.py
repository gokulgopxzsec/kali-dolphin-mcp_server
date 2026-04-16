import subprocess
import requests


def get_subdomains(domain):
    subdomains = set()

    try:
        result = subprocess.run(
            ["subfinder", "-d", domain, "-silent"],
            capture_output=True,
            text=True,
            timeout=120
        )

        for line in result.stdout.splitlines():
            line = line.strip()
            if line:
                subdomains.add(line)

    except Exception as e:
        print(f"[ERROR] Subfinder failed: {e}")

    try:
        result = subprocess.run(
            ["assetfinder", "--subs-only", domain],
            capture_output=True,
            text=True,
            timeout=120
        )

        for line in result.stdout.splitlines():
            line = line.strip()
            if line:
                subdomains.add(line)

    except Exception as e:
        print(f"[ERROR] Assetfinder failed: {e}")

    try:
        response = requests.get(
            f"https://crt.sh/?q=%25.{domain}&output=json",
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()

            for entry in data:
                name_value = entry.get("name_value", "")

                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()

                    if domain in sub:
                        subdomains.add(sub)

    except Exception as e:
        print(f"[ERROR] crt.sh failed: {e}")

    return sorted(list(subdomains))