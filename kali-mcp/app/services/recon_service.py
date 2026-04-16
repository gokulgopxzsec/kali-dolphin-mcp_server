import os
import re
import subprocess


def clean_urls(urls):
    bad_patterns = [
        "%22",
        "%0A",
        "),",
        "...",
        "gspk=",
        "gsxid=",
        "_ga=",
        "utm_",
        "facebook.com/sharer",
        "twitter.com/share",
        "mailto:",
        "javascript:",
    ]

    interesting_keywords = [
        "admin",
        "login",
        "signin",
        "signup",
        "register",
        "api",
        "graphql",
        "upload",
        "dashboard",
        "auth",
        "token",
        "callback",
        "redirect",
        "oauth",
        ".json",
        ".xml",
        ".env",
        ".well-known",
        "swagger",
        "openapi",
        "config",
        "backup",
        "test",
        "dev",
        "staging",
        "internal",
        "private",
        "debug",
        "robots.txt",
        "security.txt",
    ]

    cleaned = []

    for url in urls:
        url = url.strip()

        if not url:
            continue

        if not url.startswith(("http://", "https://")):
            continue

        if any(pattern.lower() in url.lower() for pattern in bad_patterns):
            continue

        # Remove fragments
        url = url.split("#")[0]

        # Remove trailing commas and junk characters
        url = re.sub(r'[,"\')\]]+$', "", url)

        # Remove duplicate slashes except after protocol
        url = re.sub(r'(?<!:)//+', '/', url)

        cleaned.append(url)

    # Deduplicate
    cleaned = list(set(cleaned))

    # Sort for consistency
    cleaned.sort()

    # Keep interesting URLs first
    prioritized_urls = []
    other_urls = []

    for url in cleaned:
        if any(keyword.lower() in url.lower() for keyword in interesting_keywords):
            prioritized_urls.append(url)
        else:
            other_urls.append(url)

    return prioritized_urls + other_urls[:50]