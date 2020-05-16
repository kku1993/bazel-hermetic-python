import platform
import subprocess
import sys

# Demonstrate that importing pip packages work.
# psycopg2-binary is sensitive to python minor version differences, so we're
# using it as the example.
import psycopg2

def cmd(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, _ = process.communicate()
    return out.decode('ascii').strip()


if __name__ == "__main__":
    print("Bazel python executable is", sys.executable)
    print("Bazel python version is", platform.python_version())

    print("Host python executable is", cmd(["which", "python3"]))
    print("Host python version is", cmd(["python3", "-c", "import platform; print(platform.python_version())"]))

    print("Successfully imported psycopg2-binary!")
