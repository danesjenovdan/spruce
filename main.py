import sys
from os.path import dirname, join

from dotenv import load_dotenv

from spruce.github_auth import github_login
from spruce.outdated import main as outdated
from spruce.outdated import main_all as outdated_all
from spruce.repositories import check_repositories

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def check():
    g = github_login()
    check_repositories(g, "danesjenovdan", pushed_after="2020-01-01")


if __name__ == "__main__":
    args = sys.argv[1:]

    if args:
        if args[0] == "check":
            check()
        if args[0] == "outdated":
            outdated(args[1:])
        if args[0] == "outdated-all":
            outdated_all()

    else:
        print("Usage: main.py check")
        print("Usage: main.py outdated")
        sys.exit(1)
