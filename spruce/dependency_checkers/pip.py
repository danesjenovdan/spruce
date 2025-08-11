# import re
# from os.path import basename

# import requests
# from github3.repos.repo import Repository
# from packaging.version import Version
# from packaging.version import parse as parse_version

# from .utils import Outdated, compare_versions, get_decoded_file_contents

# CHECKED_PACKAGES = [
#     "Django",
#     "wagtail",
# ]


# def _check_requirements(file_contents: str):
#     packages = []
#     lines = file_contents.splitlines()
#     for line in lines:
#         for package in CHECKED_PACKAGES:
#             if re.match(rf"^{package}([\s><=]|$)", line, re.IGNORECASE):
#                 packages.append(line)
#     return packages


# def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
#     print("Checking pip requirements / Pipfiles ...")

#     package_set = set()

#     for file in files:
#         if file_contents := get_decoded_file_contents(repo, ref, file):
#             if "requirements" in basename(file):
#                 packages = _check_requirements(file_contents)
#                 package_set.update(packages)
#             else:
#                 print(f" > No version parser for '{file}', write it!")

#     print(f" > Found: {package_set}")

#     return list(package_set)


# def _split_package_name(package_name: str) -> tuple[str, str]:
#     if match := re.search(r"==|>=|<=|<|>", package_name):
#         package_name, versions = (
#             package_name[: match.start()],
#             package_name[match.start() :],
#         )
#     else:
#         versions = "latest"
#     return package_name, versions


# def _get_effective_last_version(upper_bound: tuple) -> Version:
#     effective_last_version = list(upper_bound[:-1] + (upper_bound[-1] - 1,))
#     for i in range(len(effective_last_version) - 1, -1, -1):
#         if effective_last_version[i] < 0:
#             effective_last_version[i] = 9999
#             effective_last_version[i - 1] -= 1
#     return parse_version(".".join(map(str, effective_last_version)))


# def _parse_version_range(version_range: str) -> Version:
#     version_range = version_range.lower()
#     version_range = version_range.split(",")
#     if len(version_range) == 1 and version_range[0].startswith("=="):
#         return parse_version(version_range[0][2:])
#     if len(version_range) == 2:
#         if version_range[0].startswith(">=") and version_range[1].startswith("<"):
#             upper_bound = parse_version(version_range[1][1:]).release
#             if upper_bound[0] == 0:
#                 return None
#             return _get_effective_last_version(upper_bound)
#     return None


# def is_outdated(package_name: str) -> Outdated:
#     package_name, version_range = _split_package_name(package_name)

#     if version_range == "latest":
#         return Outdated.NO

#     version = _parse_version_range(version_range)
#     if version is None:
#         print(f" > Could not parse version range: {version_range}")
#         return Outdated.UNKNOWN

#     url = f"https://pypi.org/pypi/{package_name}/json"
#     response = requests.get(url)
#     response.raise_for_status()
#     data = response.json()
#     keys = data["releases"].keys()
#     versions = sorted(set([parse_version(key) for key in keys]), reverse=True)
#     versions = [v for v in versions if not v.is_prerelease]
#     newer_versions = [
#         v for v in versions if compare_versions(v.release, version.release)
#     ]

#     if not newer_versions:
#         return Outdated.NO

#     latest_major_version = newer_versions[0].release[0]
#     if latest_major_version > (version.release[0] + 1):
#         return Outdated.YES
#     if latest_major_version > version.release[0]:
#         return Outdated.ALMOST

#     return Outdated.MAYBE
