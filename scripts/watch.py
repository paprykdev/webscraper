import subprocess
import time
import os
import threading
from threads.prompt import prompt


def run_command(command: str) -> str:
    process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        print(f"Error running command: {command}")
        return process.stderr.decode()
    return process.stdout.decode()


thread = threading.Thread(target=prompt)


def main():
    print("Starting Docker Compose services...")
    run_command("docker compose -f ../app/docker-compose.yaml up -d")
    print("Composed!\n")
    print("Running main.py...")
    print(run_command("docker exec -it webscraper python main.py"))
    print(
        "\n\nWrite 'q' to stop program. Don't stop with 'Ctrl + C' otherwise docker container will be still on."
    )
    print("For help write 'h'.")
    print("\nWatching for changes...")
    thread.start()

    path_to_watch = "/home/paprykdev/uni/webscraper/app"
    before = {
        f: os.stat(os.path.join(path_to_watch, f)).st_mtime
        for f in os.listdir(path_to_watch)
        if f.endswith(".py")
    }

    while True:
        if threading.active_count() == 1:
            break
        time.sleep(1)
        after = {
            f: os.stat(os.path.join(path_to_watch, f)).st_mtime
            for f in os.listdir(path_to_watch)
            if f.endswith(".py")
        }
        for f in before:
            if before[f] != after[f]:
                print(f"\nDetected change in {f}")
                print("Running main.py...")
                print(run_command("docker exec -it webscraper python main.py"))
                before[f] = after[f]


if __name__ == "__main__":
    main()
