# import json
# from os.path import basename

# import nodesemver
# import requests
# from github3.repos.repo import Repository

# from .utils import Outdated, get_decoded_file_contents

# CHECKED_PACKAGES = [
#     "vue",
#     "vite",
#     "nuxt",
#     "sass",
#     "lodash",
#     "lodash-es",
#     "express",
#     "fastify",
#     # maybe add eslint, prettier, eslint-config-airbnb-base, ...
# ]


# def _check_packages(file_contents: str):
#     packages = []
#     json_data = json.loads(file_contents)
#     dependencies = json_data.get("dependencies", {})
#     dev_dependencies = json_data.get("devDependencies", {})
#     for package in CHECKED_PACKAGES:
#         if package in dependencies:
#             packages.append(f"{package}@{dependencies[package]}")
#         if package in dev_dependencies:
#             packages.append(f"{package}@{dev_dependencies[package]}")
#     return packages


# def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
#     print("Checking npm packages ...")

#     package_set = set()

#     for file in files:
#         if file_contents := get_decoded_file_contents(repo, ref, file):
#             if "package.json" in basename(file):
#                 packages = _check_packages(file_contents)
#                 package_set.update(packages)
#             else:
#                 print(f" > No version parser for '{file}', write it!")

#     print(f" > Found: {package_set}")

#     return list(package_set)


# def _split_package_name(package_name: str) -> tuple[str, str]:
#     package_name, version = package_name.rsplit("@", maxsplit=1)
#     return package_name, version


# def is_outdated(package_name: str) -> Outdated:
#     package_name, version = _split_package_name(package_name)

#     if version == "latest" or version == "*" or version == "":
#         return Outdated.NO

#     url = f"https://registry.npmjs.org/{package_name}"
#     response = requests.get(url)
#     response.raise_for_status()
#     data = response.json()
#     latest_version = data["dist-tags"]["latest"]
#     keys = data["versions"].keys()
#     versions = list(reversed(nodesemver._sorted(keys)))
#     versions = [v for v in versions if nodesemver.lte(v, latest_version, False)]
#     effective_version = nodesemver.max_satisfying(versions, version)
#     newer_versions = [v for v in versions if nodesemver.gt(v, effective_version, False)]

#     if not newer_versions:
#         return Outdated.NO

#     latest_major_version = newer_versions[0].major
#     if latest_major_version > (effective_version.major + 1):
#         return Outdated.YES
#     if latest_major_version > effective_version.major:
#         return Outdated.ALMOST

#     return Outdated.MAYBE
