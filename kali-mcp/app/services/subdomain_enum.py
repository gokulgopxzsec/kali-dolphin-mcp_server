import subprocess
 

def get_subdomains(domain):
    subdomains = set()
    subdomains.update(run_assetfinder(domain))
    subdomains.update(run_subfinder(domain))
    subdomains.update(run_crtsh(domain))

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

    return sorted(list(subdomains))