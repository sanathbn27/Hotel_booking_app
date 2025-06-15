import os
import sys
import subprocess

def main():
    # Run collectstatic
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
    # Run the main command passed to the container
    os.execvp(sys.argv[1], sys.argv[1:])

if __name__ == "__main__":
    main()