import subprocess


def get_linux_command(command: str) -> str:
    try:
        return subprocess.check_output(command.split(" ")).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return str(e)
