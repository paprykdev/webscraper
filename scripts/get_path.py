import os


def get_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = "/".join(current_path.split("/")[:-1])
    return path


def run_main():
    print(get_path())


if __name__ == "__main__":
    run_main()
