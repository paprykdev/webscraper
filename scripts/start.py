import subprocess
import os
from run_command import run_command


def main():
    docker_compose_file = os.getenv(
        "DOCKER_COMPOSE_FILE", "$WEBSCRAPER/app/docker-compose.yaml"
    )
    service_name = os.getenv("SERVICE_NAME", "webscraper")
    script_name = os.getenv("SCRIPT_NAME", "main.py")
    try:
        print("Starting Docker Compose services...\n")
        run_command(f"docker compose -f {docker_compose_file} up -d")

        print(run_command(f"docker exec {service_name} python {script_name}"))

        print("Stopping and removing Docker Compose services...")
        run_command(f"docker compose -f {docker_compose_file} down")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the script.")
        print(e)


if __name__ == "__main__":
    main()
