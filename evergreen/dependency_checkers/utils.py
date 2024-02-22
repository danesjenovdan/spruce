from github3.exceptions import NotFoundError
from github3.repos.repo import Repository


def get_decoded_file_contents(repo: Repository, ref: str, file: str) -> str | None:
    try:
        contents = repo.file_contents(file, ref)
        if type(contents.decoded) == bytes:
            return contents.decoded.decode("utf-8")
        if type(contents.decoded) == str:
            return contents.decoded
        print(f"Unknown encoding: {contents.encoding}")
        return None
    except NotFoundError:
        return None
