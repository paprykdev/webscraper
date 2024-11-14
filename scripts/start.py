import subprocess


def run_command(command: str) -> str:
    process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        print(f"Error running command: {command}")
        return process.stderr.decode()
    return process.stdout.decode()


def main():
    print("Starting Docker Compose services...\n")
    run_command("docker compose -f ../app/docker-compose.yaml up -d")

    print(run_command("docker exec -it webscraper python main.py"))

    print("Stopping and removing Docker Compose services...")
    run_command("docker compose -f ../app/docker-compose.yaml  down")


if __name__ == "__main__":
    main()
