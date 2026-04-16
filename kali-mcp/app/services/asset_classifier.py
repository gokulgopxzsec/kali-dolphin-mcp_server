def classify_asset(host):
    host_lower = host.lower()

    if "admin" in host_lower:
        return "admin panel"
    elif "api" in host_lower:
        return "api"
    elif "cdn" in host_lower or "images" in host_lower:
        return "cdn"
    elif "auth" in host_lower or "login" in host_lower:
        return "authentication"
    elif "stage" in host_lower or "staging" in host_lower:
        return "staging"
    elif "dev" in host_lower:
        return "development"
    elif "docs" in host_lower or "swagger" in host_lower:
        return "documentation"
    elif "promo" in host_lower:
        return "marketing"
    else:
        return "main website"