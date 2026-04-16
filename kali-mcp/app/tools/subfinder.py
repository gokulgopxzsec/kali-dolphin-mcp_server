import subprocess


def run_subfinder(domain):
    try:
        result = subprocess.check_output([
            'subfinder',
            '-d',
            domain,
            '-silent'
        ])
        return result.decode().splitlines()
    except Exception as e:
        return [f'Error: {e}']
