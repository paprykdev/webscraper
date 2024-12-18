import subprocess


def run_command(command: str, isPython: bool = False) -> str:
    process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return_massage = ""
    if process.returncode != 0 and not isPython:
        print(f"Error running command: {command}")
        return_massage = process.stderr.decode()
    return_massage = process.stdout.decode()
    return return_massage
