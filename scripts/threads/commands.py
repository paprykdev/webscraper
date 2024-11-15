from run_command import run_command


def quitCondition(command: str) -> bool:
    return command in ["q", "quit", "exit", "stop"]


def quitService(path: str):
    print("Stopping and removing Docker Compose services...")
    run_command(f"docker compose -f {path}/app/docker-compose.yaml down")
    return None


def helpCondition(command: str) -> bool:
    return command in ["h", "help"]


def clearCondition(command: str) -> bool:
    return command in ["c", "clear", "cls"]


def systemCommand(command: str) -> str:
    words = command[1:].split()
    if words[0] == "":
        return "Command not found. Write 'h' for help."
    print(
        run_command(
            f'docker exec -it webscraper {" ".join(words)}',
        )
    )
    return None


def restartCondition(command: str) -> bool:
    return command in ["r", "restart"]


def restartService(path: str):
    print("Restarting Docker Compose services...")
    run_command(f"docker compose -f {path}/app/docker-compose.yaml down")
    run_command(f"docker compose -f {path}/app/docker-compose.yaml up -d")
    print("Composed!")
    return None


def runCondition(command: str) -> bool:
    return command in ["run"]


def runService():
    print("Running main.py...")
    print(
        run_command(
            "docker exec -it webscraper python main.py",
        )
    )
    return None
