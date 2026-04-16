import subprocess


def get_wayback_urls(domain):
    urls = []

    try:
        result = subprocess.run(
            ["waybackurls", domain],
            capture_output=True,
            text=True,
            timeout=120
        )

        for line in result.stdout.splitlines():
            line = line.strip()

            if line:
                urls.append(line)

    except Exception as e:
        print(f"[ERROR] Wayback scan failed: {e}")

    return list(set(urls))