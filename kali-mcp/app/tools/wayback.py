import subprocess


def run_wayback(domain):
    try:
        result = subprocess.check_output([
            'waybackurls',
            domain
        ])
        return result.decode().splitlines()
    except Exception as e:
        return [f'Error: {e}']
