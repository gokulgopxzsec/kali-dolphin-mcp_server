from fastapi import APIRouter
from app.services.asset_classifier import classify_asset
from app.services.report_generator import generate_report

router = APIRouter()


@router.post("/scan")
def scan_target(target: str):
    recon_data = run_recon(target)

    urls = recon_data.get("urls", [])
    live_hosts = recon_data.get("live_hosts", [])

    scored_urls = score_urls(urls)

    screenshots = capture_screenshots([
        host.split(" ")[0] for host in live_hosts
    ])

    fuzzing_results = []
    for item in scored_urls[:5]:
        if item["score"] >= 8:
            fuzzing_results.append(fuzz_url(item["url"]))

    js_results = []
    for item in scored_urls[:5]:
        js_results.append(run_js_recon(item["url"]))

    classified_assets = []
    for host in live_hosts:
        clean_host = host.split(" ")[0]
        classified_assets.append({
            "host": clean_host,
            "type": classify_asset(clean_host)
        })

    nuclei_data = run_nuclei(target)

    report_data = generate_report(
        target,
        recon_data,
        nuclei_data,
        scored_urls,
        screenshots,
        classified_assets
    )

    return {
        "target": target,
        "recon": recon_data,
        "top_scored_urls": scored_urls[:20],
        "screenshots": screenshots,
        "fuzzing_results": fuzzing_results,
        "js_results": js_results,
        "classified_assets": classified_assets,
        "nuclei": nuclei_data,
        "reports": report_data
    }