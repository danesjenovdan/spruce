import re
from os.path import basename
import json
from github3.repos.repo import Repository

from .utils import get_decoded_file_contents

CHECKED_PACKAGES = [
    "vue",
    "vite",
    "nuxt",
    "sass",
    "lodash",
    "lodash-es",
    "express",
    "fastify",
    # maybe add eslint, prettier, eslint-config-airbnb-base, ...
]


def _check_packages(file_contents: str):
    packages = []
    json_data = json.loads(file_contents)
    dependencies = json_data.get("dependencies", {})
    dev_dependencies = json_data.get("devDependencies", {})
    for package in CHECKED_PACKAGES:
        if package in dependencies:
            packages.append(f"{package}@{dependencies[package]}")
        if package in dev_dependencies:
            packages.append(f"{package}@{dev_dependencies[package]}")
    return packages


def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
    print("Checking npm packages ...")

    package_set = set()

    for file in files:
        if file_contents := get_decoded_file_contents(repo, ref, file):
            if "package.json" in basename(file):
                packages = _check_packages(file_contents)
                package_set.update(packages)
            else:
                print(f" > No version parser for '{file}', write it!")

    print(f" > Found: {package_set}")

    return list(package_set)
