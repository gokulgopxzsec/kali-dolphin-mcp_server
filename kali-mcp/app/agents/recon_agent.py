from urllib.parse import urlparse

from app.services.subdomain_enum import get_subdomains
from app.services.http_probe import probe_hosts
from app.services.nuclei_scan import run_nuclei_on_hosts
from app.services.ffuf_scan import run_ffuf, should_fuzz
from app.services.screenshot import take_screenshots
from app.services.scoring import score_target


def run_recon(target,prompt=None):
    domain = urlparse(target).netloc.replace("www.", "")

    print(f"[INFO] Recon prompt: {prompt}")

    try:
        subdomains = get_subdomains(domain)
    except Exception as e:
        print(f"[ERROR] Subdomain enumeration failed: {e}")
        subdomains = [domain]

    try:
        live_hosts = probe_hosts(subdomains)
    except Exception as e:
        print(f"[ERROR] HTTP probe failed: {e}")
        live_hosts = []

    scored_hosts = []

    for host in live_hosts:
        clean_host = host.split(" ")[0]

        try:
            score_data = score_target(clean_host)

            scored_hosts.append({
                "host": clean_host,
                "score": score_data.get("score", 0),
                "reasons": score_data.get("reasons", [])
            })
        except Exception as e:
            print(f"[ERROR] Scoring failed for {clean_host}: {e}")

            scored_hosts.append({
                "host": clean_host,
                "score": 0,
                "reasons": []
            })

    scored_hosts = sorted(
        scored_hosts,
        key=lambda x: x["score"],
        reverse=True
    )

    try:
        screenshot_dir = take_screenshots(live_hosts)
    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")
        screenshot_dir = None

    try:
        nuclei_results = run_nuclei_on_hosts(live_hosts)
    except Exception as e:
        print(f"[ERROR] Nuclei scan failed: {e}")
        nuclei_results = []

    ffuf_results = []

    for host_data in scored_hosts:
        host = host_data["host"]

        try:
            if should_fuzz(host):
                ffuf_output = run_ffuf(host)

                ffuf_results.append({
                    "host": host,
                    "output": ffuf_output
                })
        except Exception as e:
            print(f"[ERROR] FFUF failed for {host}: {e}")

    return {
        "domain": domain,
        "subdomains": subdomains,
        "live_hosts": live_hosts,
        "high_risk_hosts": scored_hosts,
        "screenshots": screenshot_dir,
        "nuclei": nuclei_results,
        "ffuf": ffuf_results
    }