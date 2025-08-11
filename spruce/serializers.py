from os import makedirs
from os.path import dirname
from typing import Any, TypeVar

import msgspec

T = TypeVar("T")


def save_json(item: Any, path: str) -> None:
    serialized = msgspec.json.encode(item)
    serialized = msgspec.json.format(serialized, indent=2)

    makedirs(dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(serialized)


def load_json(path: str, type: type[T]) -> T | None:
    try:
        with open(path, "rb") as f:
            return msgspec.json.decode(f.read(), type=type)
    except (FileNotFoundError, msgspec.DecodeError):
        return None
