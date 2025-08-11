from os.path import basename

from github3.git import Hash, Tree

from .structs import DepFileEntry


def is_docker(entry: Hash) -> bool:
    filename: str = basename(entry.path)
    # match partial filenames (e.g. Dockerfile.dev, dev.Dockerfile, etc.)
    return (
        "Dockerfile" in filename
        or filename.endswith("compose.yaml")
        or filename.endswith("compose.yml")
    )


def is_pip(entry: Hash) -> bool:
    filename: str = basename(entry.path)
    return (
        filename == "requirements.txt"
        or filename == "Pipfile"
        or filename == "Pipfile.lock"
    )


def is_npm(entry: Hash) -> bool:
    if "node_modules/" in entry.path:
        return False
    if "bower_components/" in entry.path:
        return False
    filename: str = basename(entry.path)
    return (
        filename == "package.json"
        or filename == "package-lock.json"
        or filename == "yarn.lock"
        or filename == "pnpm-lock.yaml"
    )


def find_dependency_files(tree: Tree) -> list[DepFileEntry]:
    deps = []

    for entry in tree.tree:
        # blob is a file, tree is a directory
        if entry.type != "blob":
            continue
        if is_docker(entry):
            deps.append(DepFileEntry(path=entry.path, type="docker"))
        if is_pip(entry):
            deps.append(DepFileEntry(path=entry.path, type="pip"))
        if is_npm(entry):
            deps.append(DepFileEntry(path=entry.path, type="npm"))
    return deps
