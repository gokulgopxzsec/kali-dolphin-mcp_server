import subprocess
import tempfile

HTTPX_PATH = r"C:\Users\gokul\go\bin\httpx.exe"


def run_httpx(subdomains):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("\n".join(subdomains))
        tmp.flush()

        try:
            result = subprocess.check_output([
                HTTPX_PATH,
                "-l",
                tmp.name,
                "-silent"
            ])
            return result.decode().splitlines()
        except Exception as e:
            return [f"Error: {e}"]