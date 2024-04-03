import json

from .dependency_checkers.docker import is_outdated as is_outdated_docker
from .dependency_checkers.pip import is_outdated as is_outdated_pip
from .dependency_checkers.npm import is_outdated as is_outdated_npm


def check_outdated(repo_name):
    print(f"Checking outdated packages for {repo_name}")

    with open("results.json", "r") as f:
        results = json.load(f)
    repo_result = next(filter(lambda x: x["repo"] == repo_name, results), None)

    if repo_result is None:
        print(f"Repo {repo_name} not found in results.json")
        return

    versions = repo_result.get("versions", {})
    if "docker" in versions:
        for image in versions["docker"]:
            print(f"{image} = {is_outdated_docker(image)}")
    if "pip" in versions:
        for package in versions["pip"]:
            print(f"{package} = {is_outdated_pip(package)}")
    if "npm" in versions:
        for package in versions["npm"]:
            print(f"{package} = {is_outdated_npm(package)}")


def main(args):
    if len(args) >= 1:
        check_outdated(args[0])
    else:
        print("Usage: main.py outdated repo-name")
