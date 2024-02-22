from github3.repos.repo import Repository

from .utils import get_decoded_file_contents


def _check_dockerfile(file_contents: str):
    images = []
    lines = file_contents.splitlines()
    for line in lines:
        if line.startswith("FROM "):
            image = line.split(" ")[1]
            images.append(image)
    return images


def check(repo: Repository, ref: str, files: list[str]) -> list[str]:
    print("Checking Dockerfiles ...")

    image_set = set()

    for file in files:
        if file_contents := get_decoded_file_contents(repo, ref, file):
            images = _check_dockerfile(file_contents)
            image_set.update(images)

    print(f" > Found: {image_set}")

    return list(image_set)
