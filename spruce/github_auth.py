import os

import github3


def github_login() -> github3.GitHub:
    token = os.getenv("GH_TOKEN")
    if not token:
        raise ValueError("GH_TOKEN environment variable is not set")

    github_connection = github3.login(token=token)
    if not github_connection:
        raise ValueError("GH_TOKEN is invalid")

    return github_connection
