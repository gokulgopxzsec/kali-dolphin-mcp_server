HIGH_RISK_KEYWORDS = [
    "admin",
    "staging",
    "stage",
    "dev",
    "test",
    "internal",
    "dashboard",
    "api",
    "graphql",
    "swagger",
    "jenkins",
    "grafana",
    "kibana",
    "phpmyadmin",
    "actuator",
    "debug",
    "metrics",
    "login",
]


def score_target(url):
    score = 0
    matched_keywords = []

    lowered = url.lower()

    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in lowered:
            score += 5
            matched_keywords.append(keyword)

    if lowered.startswith("https://"):
        score += 2

    if any(x in lowered for x in [".env", "swagger", "graphql", "actuator"]):
        score += 10

    return {
        "url": url,
        "score": score,
        "matched_keywords": matched_keywords
    }


def score_target(host):
    score = 0
    reasons = []

    keywords = {
        "admin": 10,
        "api": 8,
        "dev": 7,
        "stage": 7,
        "staging": 7,
        "internal": 9,
        "dashboard": 8,
        "portal": 6,
        "auth": 6,
        "login": 5,
        "jenkins": 10,
        "grafana": 9,
        "kibana": 9,
        "graphql": 8,
        "swagger": 10
    }

    host_lower = host.lower()

    for keyword, value in keywords.items():
        if keyword in host_lower:
            score += value
            reasons.append(f"Matched keyword: {keyword}")

    if host.startswith("https://"):
        score += 2
        reasons.append("Uses HTTPS")

    return {
        "score": score,
        "reasons": reasons
    }