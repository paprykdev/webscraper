import subprocess
import os
from run_command import run_command
from get_path import get_path


def run_main():
    path = get_path()
    try:
        result = run_command(f"python3 {path}/app/main.py")
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")


if __name__ == "__main__":
    run_main()
