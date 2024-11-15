import sys
from threads.commands import *
from run_command import run_command
from get_path import get_path
from threads.help_list import help_list


def prompt():
    while True:
        command = input("> ")
        if quitCondition(command):
            quitService(get_path())
            break
        if helpCondition(command):
            print(help_list())
            continue
        if clearCondition(command):
            clearScreen()
            continue
        if command.startswith("$"):
            systemCommand(command)
            continue
        if restartCondition(command):
            restartService(get_path())
            continue
        if runCondition(command):
            runService()
            continue
        if command == "":
            continue
        else:
            print("Command not found. Write 'h' for help.")
            continue
    sys.exit(0)
