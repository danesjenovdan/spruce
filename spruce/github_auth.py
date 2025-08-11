import os

from github3 import GitHub


def github_login() -> GitHub:
    token = os.getenv("GH_TOKEN")
    if not token:
        raise ValueError("GH_TOKEN environment variable is not set")

    github_connection = GitHub(token=token)
    if not github_connection:
        raise ValueError("GH_TOKEN is invalid")

    return github_connection
