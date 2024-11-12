import subprocess
import time


def run_command(command):
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr.decode())
    return result.stdout.decode()


def wait_for_webscraper():
    while True:
        result = run_command("docker compose ps -q webscraper")
        container_id = result.strip()

        if not container_id:
            print("Webscraper container not found.")
            break

        status = run_command(
            f"docker inspect --format '{{.State.Status}}' {container_id}"
        )

        if status.strip() == "exited":
            print("Webscraper has finished.")
            break

        print("Waiting for webscraper to finish...")
        time.sleep(3)


def main():
    print("Starting Docker Compose services...")
    run_command("docker compose up -d")

    wait_for_webscraper()

    print("Stopping and removing Docker Compose services...")
    run_command("docker compose down")


if __name__ == "__main__":
    main()
