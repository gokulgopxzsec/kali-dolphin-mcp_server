import re
import requests


def extract_js_files(urls):
    js_files = set()

    for url in urls:
        try:
            response = requests.get(url, timeout=10)

            matches = re.findall(r'https?://[^"\']+\.js|/[^"\']+\.js', response.text)

            for match in matches:
                js_files.add(match)

        except Exception:
            pass

    return list(js_files)