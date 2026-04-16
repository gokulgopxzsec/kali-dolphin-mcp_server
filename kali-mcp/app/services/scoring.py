INTERESTING_KEYWORDS = {
    "grafana": 10,
    "kibana": 10,
    "actuator": 9,
    "debug": 8,
    "metrics": 8,
    "internal": 7,
    "staging": 8,
    "dev": 7,
    ".env": 10,
    ".git": 10,
    ".well-known": 6,
    "upload": 8,
    "phpinfo": 9,
}

IGNORE_PARAMS = [
    "utm_",
    "gclid",
    "gspk",
    "gsxid",
    "fbclid",
    "_ga",
]


def score_target(host):
    score = 0
    reasons = []

    host_lower = host.lower()

    if "admin" in host_lower:
        score += 40
        reasons.append("Contains admin keyword")

    if "api" in host_lower:
        score += 20
        reasons.append("Contains api keyword")

    if "dev" in host_lower:
        score += 15
        reasons.append("Contains dev keyword")

    if "staging" in host_lower:
        score += 15
        reasons.append("Contains staging keyword")

    return {
        "score": score,
        "reasons": reasons
    }

def should_ignore_url(url: str):
    url_lower = url.lower()

    for param in IGNORE_PARAMS:
        if param in url_lower:
            return True

    if len(url) > 300:
        return True

    if "%22" in url or "%0a" in url:
        return True

    return False