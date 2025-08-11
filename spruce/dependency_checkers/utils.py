# from enum import Enum

# from github3.exceptions import NotFoundError
# from github3.repos.repo import Repository


# class Outdated(Enum):
#     UNKNOWN = -1
#     NO = 0
#     MAYBE = 1
#     ALMOST = 2
#     YES = 3


# def get_decoded_file_contents(repo: Repository, ref: str, file: str) -> str | None:
#     try:
#         contents = repo.file_contents(file, ref)
#         if type(contents.decoded) == bytes:
#             return contents.decoded.decode("utf-8")
#         if type(contents.decoded) == str:
#             return contents.decoded
#         print(f"Unknown encoding: {contents.encoding}")
#         return None
#     except NotFoundError:
#         return None


# def compare_versions(a: tuple, b: tuple) -> bool:
#     if len(a) == len(b):
#         return a > b
#     if len(a) > len(b):
#         return a[: len(b)] > b
#     return a > b[: len(a)]
