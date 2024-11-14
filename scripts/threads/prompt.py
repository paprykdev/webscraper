import commands
import subprocess
import sys
import threading


def prompt():
    while True:
        command = input("> ")
        if commands.quitCondition(command):
            print("Stopping and removing Docker Compose services...")
            subprocess.run(
                "docker compose -f ../app/docker-compose.yaml down",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            break
        if commands.helpCondition(command):
            print(
                """
["h", "help"], - for help.
["q", "quit", "exit", "stop"], - to stop program.
["c", "clear", "cls"], - to clear console.
["r", "restart"], - to restart Docker Compose services.
["run"], - to run main.py in docker container.
["$..."], - to evaluate command in docker container.
"""
            )
            continue
        if commands.clearCondition(command):
            print("\n" * 100)
            continue
        if command.startswith("$"):
            print(commands.systemCommand(command))
            continue
        if commands.restartCondition(command):
            print("Restarting Docker Compose services...")
            subprocess.run(
                "docker compose -f ../app/docker-compose.yaml down",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            subprocess.run(
                "docker compose -f ../app/docker-compose.yaml up -d",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Composed!")
            continue
        if commands.runCondition(command):
            print("Running main.py...")
            print(
                subprocess.run(
                    "docker exec -it webscraper python main.py",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).stdout.decode()
            )
            continue
        if command == "":
            continue
        else:
            print("Command not found. Write 'h' for help.")
            continue
    sys.exit(0)
