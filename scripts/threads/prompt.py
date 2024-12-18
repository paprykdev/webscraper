import sys
from threads.commands import *
from run_command import run_command
from get_path import get_path
from threads.help_list import help_list
import time


def prompt():
    while True:
        try:
            command = input("> ")
            if quitCondition(command):
                quitService(get_path())
                break
            elif helpCondition(command):
                print(help_list())
            elif clearCondition(command):
                clearScreen()
            elif command.startswith("$"):
                systemCommand(command)
            elif restartCondition(command):
                restartService(get_path())
            elif runCondition(command):
                runService()
            elif command == "":
                pass
            else:
                print(f"Command: {command} not found. Write 'h' for help.")
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            quitService(get_path())
    sys.exit(0)
