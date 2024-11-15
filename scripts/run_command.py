import subprocess
import sys


def run_command(command: str) -> str:
    process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        print(f"Error running command: {command}")
        print(process.stderr.decode())
        sys.exit(process.returncode)
    return process.stdout.decode()
