import subprocess
import os
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


def main():
    docker_compose_file = os.getenv("DOCKER_COMPOSE_FILE", "./app/docker-compose.yaml")
    service_name = os.getenv("SERVICE_NAME", "webscraper")
    script_name = os.getenv("SCRIPT_NAME", "main.py")

    print("Starting Docker Compose services...\n")
    run_command(f"docker compose -f {docker_compose_file} up -d")

    print(run_command(f"docker exec {service_name} python {script_name}"))

    print("Stopping and removing Docker Compose services...")
    run_command(f"docker compose -f {docker_compose_file} down")


if __name__ == "__main__":
    main()
