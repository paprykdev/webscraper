import time
import os
import threading
from threads.prompt import prompt
from run_command import run_command
from get_path import get_path

thread = threading.Thread(target=prompt)


def main():
    path = get_path()
    docker_compose_file = os.getenv(
        "DOCKER_COMPOSE_FILE", f"{path}/app/docker-compose.yaml"
    )
    print("Starting Docker Compose services...")
    run_command(f"docker compose -f {docker_compose_file} up -d")
    print("Composed!\n")
    print("Running main.py...")
    print(run_command("docker exec -it webscraper python main.py"))
    print(
        "\n\nWrite 'q' to stop program. Don't stop with 'Ctrl + C' otherwise docker container will be still on."
    )
    print("For help write 'h'.")
    print("\nWatching for changes...")
    thread.start()

    before = {
        f: os.stat(os.path.join(path, "app", f)).st_mtime
        for f in os.listdir(os.path.join(path, "app"))
        if f.endswith(".py")
    }

    while True:
        if threading.active_count() == 1:
            break
        time.sleep(1)
        after = {
            f: os.stat(os.path.join(path, "app", f)).st_mtime
            for f in os.listdir(os.path.join(path, "app"))
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
