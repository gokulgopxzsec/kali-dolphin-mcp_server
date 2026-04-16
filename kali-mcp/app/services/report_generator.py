import json
import os
from datetime import datetime

from app.config import REPORT_DIR


def generate_report(
    target,
    recon_data,
    nuclei_data,
    scored_urls,
    screenshots,
    classified_assets
):
    os.makedirs(REPORT_DIR, exist_ok=True)

    safe_target = (
        target.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
    )

    report_path = os.path.join(REPORT_DIR, f"{safe_target}_report.md")
    json_path = os.path.join(REPORT_DIR, f"{safe_target}_report.json")

    markdown = f"""# Recon Report

## Target
{target}

## Generated
{datetime.now()}

## Subdomains
{len(recon_data.get('subdomains', []))}

## Live Hosts
{len(recon_data.get('live_hosts', []))}

## Interesting URLs
{len(scored_urls)}

## Top Ranked URLs
"""

    for item in scored_urls[:20]:
        markdown += (
            f"- Score {item['score']} | "
            f"{item['url']} | "
            f"Keywords: {', '.join(item['matched_keywords'])}\n"
        )

    markdown += "\n## Asset Classification\n"

    for asset in classified_assets:
        markdown += f"- {asset['host']} → {asset['type']}\n"

    markdown += "\n## Nuclei Findings\n"

    for finding in nuclei_data.get("findings", [])[:50]:
        markdown += f"- {finding}\n"

    markdown += "\n## Screenshots\n"

    for screenshot in screenshots:
        markdown += f"- {screenshot}\n"

    markdown += "\n## Recommended Manual Checks\n"
    markdown += "- Check admin and staging panels manually\n"
    markdown += "- Review exposed JS files for secrets\n"
    markdown += "- Review Swagger, GraphQL, and Actuator endpoints\n"
    markdown += "- Investigate high-risk hosts first\n"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "target": target,
                "recon": recon_data,
                "nuclei": nuclei_data,
                "scored_urls": scored_urls,
                "screenshots": screenshots,
                "classified_assets": classified_assets,
            },
            f,
            indent=4
        )

    return {
        "markdown_report": report_path,
        "json_report": json_path
    }