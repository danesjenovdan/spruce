import re
from os.path import basename

from github3.repos.repo import Repository

from .utils import get_decoded_file_contents

CHECKED_PACKAGES = [
    "Django",
    "wagtail",
]


def _check_requirements(file_contents: str):
    packages = []
    lines = file_contents.splitlines()
    for line in lines:
        for package in CHECKED_PACKAGES:
            if re.match(rf"^{package}([\s><=]|$)", line, re.IGNORECASE):
                packages.append(line)
    return packages


def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
    print("Checking pip requirements / Pipfiles ...")

    package_set = set()

    for file in files:
        if file_contents := get_decoded_file_contents(repo, ref, file):
            if "requirements" in basename(file):
                packages = _check_requirements(file_contents)
                package_set.update(packages)
            else:
                print(f" > No version parser for '{file}', write it!")

    print(f" > Found: {package_set}")

    return list(package_set)
