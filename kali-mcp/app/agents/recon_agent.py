from urllib.parse import urlparse

from app.agents.prompt_agent import parse_prompt
from app.services.subdomain_enum import get_subdomains
from app.services.http_probe import probe_hosts
from app.services.nuclei_scan import run_nuclei_on_hosts
from app.services.ffuf_scan import run_ffuf, should_fuzz
from app.services.screenshot import take_screenshots
from app.services.scoring import score_target
from app.services.katana_scan import run_katana
from app.services.wayback_scan import get_wayback_urls
from app.services.js_extractor import extract_js_files
from app.services.port_scan import run_naabu
from app.services.wordlists import PROMPT_WORDLIST_MAP


def run_recon(target, prompt=None):
    domain = urlparse(target).netloc.replace("www.", "")
    prompt_flags = parse_prompt(prompt or "")
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
        clean_host = host.split(" ")[0].strip()

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

    scored_hosts = sorted(scored_hosts, key=lambda x: x["score"], reverse=True)

    try:
        screenshot_dir = take_screenshots(live_hosts)
    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")
        screenshot_dir = None

    try:
        nuclei_results = run_nuclei_on_hosts(live_hosts)
    except Exception as e:
        print(f"[ERROR] Nuclei scan failed: {e}")
        nuclei_results = {"status": "error", "message": str(e), "findings": []}

    ffuf_results = []
    katana_results = []
    wayback_results = []
    port_results = []
    js_files = []

    for host_data in scored_hosts:
        host = host_data["host"]

        try:
            if should_fuzz(host):
                wordlist = PROMPT_WORDLIST_MAP["common"]

                if prompt_flags.get("admin"):
                    wordlist = PROMPT_WORDLIST_MAP.get("admin", wordlist)
                elif prompt_flags.get("api"):
                    wordlist = PROMPT_WORDLIST_MAP.get("api", wordlist)
                elif prompt_flags.get("login"):
                    wordlist = PROMPT_WORDLIST_MAP.get("login", wordlist)
                elif prompt_flags.get("upload"):
                    wordlist = PROMPT_WORDLIST_MAP.get("upload", wordlist)

                ffuf_output = run_ffuf(host, wordlist)
                ffuf_results.append({
                    "host": host,
                    "wordlist": wordlist,
                    "output": ffuf_output
                })
        except Exception as e:
            print(f"[ERROR] FFUF failed for {host}: {e}")

        try:
            if prompt_flags.get("crawl"):
                katana_output = run_katana(host)
                katana_results.append({
                    "host": host,
                    "urls": katana_output.get("urls", [])
                })

                if prompt_flags.get("javascript"):
                    js_output = extract_js_files(katana_output.get("urls", []))
                    js_files.extend(js_output)
        except Exception as e:
            print(f"[ERROR] Katana/JS failed for {host}: {e}")

        try:
            if prompt_flags.get("ports"):
                ports_output = run_naabu(host)
                port_results.append({
                    "host": host,
                    "ports": ports_output.get("ports", [])
                })
        except Exception as e:
            print(f"[ERROR] Port scan failed for {host}: {e}")

    try:
        if prompt_flags.get("historical"):
            wayback_results = get_wayback_urls(domain)
    except Exception as e:
        print(f"[ERROR] Historical URL collection failed: {e}")
        wayback_results = {"status": "error", "message": str(e), "urls": []}

    return {
        "domain": domain,
        "prompt": prompt,
        "prompt_flags": prompt_flags,
        "subdomains": subdomains,
        "live_hosts": live_hosts,
        "high_risk_hosts": scored_hosts,
        "screenshots": screenshot_dir,
        "nuclei": nuclei_results,
        "ffuf": ffuf_results,
        "katana": katana_results,
        "wayback": wayback_results,
        "ports": port_results,
        "js_files": sorted(list(set(js_files)))
    }