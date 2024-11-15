import os
from run_command import run_command


def get_path():
    pwd = run_command("pwd")
    splitted = pwd.split("/")
    splitted[-1] = splitted[-1].replace("\n", "")

    print(splitted[: splitted.index("webscraper") + 1])

    if splitted.count("webscraper") > 1 and "webscraper" in splitted:
        for i in range(len(splitted) - 1, -1, -1):
            potential_path = "/".join(splitted[: i + 1])
            if "webscraper" in potential_path:
                script_path = f"{potential_path}/scripts"
                if os.path.isdir(script_path):
                    return potential_path
                else:
                    return "This is not a valid webscraper project."
    else:
        return "/".join(splitted[: splitted.index("webscraper") + 1])


def run_main():
    print(get_path())


if __name__ == "__main__":
    run_main()
