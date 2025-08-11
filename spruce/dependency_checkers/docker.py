# import re

# import requests
# from github3.repos.repo import Repository

# from .utils import Outdated, compare_versions, get_decoded_file_contents


# def _check_dockerfile(file_contents: str):
#     images = []
#     lines = file_contents.splitlines()
#     for line in lines:
#         if line.startswith("FROM "):
#             image = line.split(" ")[1]
#             images.append(image)
#     return images


# def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
#     print("Checking Dockerfiles ...")

#     image_set = set()

#     for file in files:
#         if file_contents := get_decoded_file_contents(repo, ref, file):
#             images = _check_dockerfile(file_contents)
#             image_set.update(images)

#     print(f" > Found: {image_set}")

#     return list(image_set)


# def _remove_domain_from_image_name(image_name: str) -> str:
#     i = image_name.find("/")
#     if i != -1:
#         part = image_name[:i]
#         if ":" in part or "." in part or part == "localhost":
#             image_name = image_name[i + 1 :]
#     return image_name


# def _split_image_name(image_name: str) -> tuple[str, str, str]:
#     if ":" in image_name:
#         image_name, tag = image_name.rsplit(":", 1)
#     else:
#         tag = "latest"

#     if "/" in image_name:
#         repository, name = image_name.rsplit("/", 1)
#     else:
#         repository = "library"
#         name = image_name

#     return repository, name, tag


# def _get_version_from_tag(tag: str) -> tuple:
#     tag = tag.lower()
#     if tag.startswith("v") and len(tag) > 1 and tag[1].isdigit():
#         tag = tag[1:]

#     if tag[0].isdigit():
#         version_string = tag
#         if "-" in tag:
#             version_string, extra = tag.split("-", 1)
#             if re.match(r"^rc(-|$)", extra):
#                 return (0,)  # ignore pre-releases

#         if match := re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_string):
#             major, minor, patch = map(int, match.groups())
#             return (major, minor, patch)
#         elif match := re.match(r"^(\d+)\.(\d+)$", version_string):
#             major, minor = map(int, match.groups())
#             return (major, minor)
#         elif match := re.match(r"^(\d+)$", version_string):
#             major = int(match.group())
#             return (major,)
#     return (0,)


# def is_outdated(image_name: str) -> Outdated:
#     image_name = _remove_domain_from_image_name(image_name)
#     repository, name, tag = _split_image_name(image_name)

#     if tag == "latest":
#         return Outdated.NO

#     version = _get_version_from_tag(tag)
#     if len(version) == 1 and version[0] == 0:
#         print(f" > Could not parse version: {tag}")
#         return Outdated.UNKNOWN

#     url = f"https://hub.docker.com/v2/repositories/{repository}/{name}/tags?page_size=100&page=1"
#     response = requests.get(url)
#     response.raise_for_status()
#     data = response.json()
#     tags = [tag["name"] for tag in data["results"]]
#     versions = sorted(set([_get_version_from_tag(tag) for tag in tags]), reverse=True)
#     newer_versions = [v for v in versions if compare_versions(v, version)]

#     if not newer_versions:
#         return Outdated.NO

#     if name == "python":
#         # check minor versions
#         newer_minor_versions = [v for v in newer_versions if len(v) > 1]
#         latest_minor_version = newer_minor_versions[0][1] if newer_minor_versions else 0
#         if latest_minor_version > (version[1] + 1):
#             return Outdated.YES
#         if latest_minor_version > version[1]:
#             return Outdated.ALMOST
#     else:
#         # check major versions
#         latest_major_version = newer_versions[0][0]
#         if latest_major_version > (version[0] + 1):
#             return Outdated.YES
#         if latest_major_version > version[0]:
#             return Outdated.ALMOST

#     return Outdated.MAYBE
