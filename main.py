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
    print("=== Bazel Python ===")
    print(sys.executable)
    print(sys.version)

    print("=== Host Python ===")
    print(cmd(["which", "python3"]))
    print(cmd(["python3", "-c", "import sys; print(sys.version)"]))

    print("=== Pip Package ===")
    print("Successfully imported psycopg2-binary!")
