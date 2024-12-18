import subprocess
import os
from run_command import run_command
from get_path import get_path


def main():
    try:
        docker_compose_file = os.getenv(
            "DOCKER_COMPOSE_FILE", f"{get_path()}/app/docker-compose.yaml"
        )
        service_name = os.getenv("SERVICE_NAME", "scraper")
        script_name = os.getenv("SCRIPT_NAME", "main.py")
        try:
            print("Starting Docker Compose services...\n")
            run_command(f"docker compose -f {docker_compose_file} up -d")

            print(run_command(f"docker exec -it {service_name} xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' python3 {script_name}"))

            print("Stopping and removing Docker Compose services...")
            run_command(f"docker compose -f {docker_compose_file} down")
        except subprocess.CalledProcessError as e:
            print("An error occurred while running the script.")
            print(e)
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
            run_command(f"docker compose -f {docker_compose_file} down")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        run_command(f"docker compose -f {docker_compose_file} down")


if __name__ == "__main__":
    main()
