def parse_prompt(prompt):
    prompt = prompt.lower()

    return {
        "admin": any(word in prompt for word in ["admin", "dashboard", "panel"]),
        "api": "api" in prompt,
        "login": any(word in prompt for word in ["login", "signin", "auth"]),
        "upload": "upload" in prompt,
        "historical": any(word in prompt for word in ["history", "historical", "wayback", "old"]),
        "javascript": any(word in prompt for word in ["javascript", "js", "endpoint"]),
        "ports": any(word in prompt for word in ["port", "nmap", "naabu"]),
        "crawl": any(word in prompt for word in ["crawl", "crawler", "katana"]),
        "params": any(word in prompt for word in ["parameter", "params", "query"]),
    }