# from collections import defaultdict
# from os.path import basename


# def is_dockerfile(entry):
#     filename = basename(entry.path)
#     # match partial filenames (e.g. Dockerfile.dev, dev.Dockerfile, etc.)
#     return "Dockerfile" in filename


# def is_pip(entry):
#     filename = basename(entry.path)
#     return (
#         filename == "requirements.txt"
#         or filename == "Pipfile"
#         or filename == "Pipfile.lock"
#     )


# def is_npm(entry):
#     if "node_modules/" in entry.path:
#         return False
#     if "bower_components/" in entry.path:
#         return False
#     filename = basename(entry.path)
#     return (
#         filename == "package.json"
#         or filename == "package-lock.json"
#         or filename == "yarn.lock"
#         or filename == "pnpm-lock.yaml"
#     )


# def find_dependency_files(tree):
#     deps = defaultdict(list)
#     for entry in tree.tree:
#         # blob is a file, tree is a directory
#         if entry.type != "blob":
#             continue
#         if is_dockerfile(entry):
#             deps["docker"].append(entry.path)
#         if is_pip(entry):
#             deps["pip"].append(entry.path)
#         if is_npm(entry):
#             deps["npm"].append(entry.path)
#     return deps
