import platform
import subprocess
import sys

# Demonstrate that importing pip packages work.
from baseconv import base62

def cmd(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, _ = process.communicate()
    return out


if __name__ == "__main__":
    print("My python executable is", sys.executable)
    print("My python version is", platform.python_version())

    print("The host's python executable is", cmd(["which", "python3"]))
    print("The host's python version is", cmd(["python3", "--version"]))
