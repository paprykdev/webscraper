import subprocess


def quitCondition(command: str) -> bool:
    return command in ["q", "quit", "exit", "stop"]


def helpCondition(command: str) -> bool:
    return command in ["h", "help"]


def clearCondition(command: str) -> bool:
    return command in ["c", "clear", "cls"]


def systemCommand(command: str) -> str:
    words = command[slice(1, len(command))].split()
    if words[0] == "":
        return "Command not found. Write 'h' for help."
    return subprocess.run(
        f'docker exec -it webscraper {" ".join(words)}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.decode()


def restartCondition(command: str) -> bool:
    return command in ["r", "restart"]


def runCondition(command: str) -> bool:
    return command in ["run"]
