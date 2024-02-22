from os.path import dirname, join

from dotenv import load_dotenv

from evergreen.github_auth import github_login
from evergreen.repositories import check_repositories

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():
    g = github_login()
    check_repositories(g, "danesjenovdan", pushed_after="2020-01-01")


if __name__ == "__main__":
    main()
