from enum import Enum
from typing import Literal

import msgspec


class RepoToCheck(msgspec.Struct):
    owner: str
    name: str
    created_at: str
    pushed_at: str
    default_branch: str
    check_branches: list[str]


class DepFileEntry(msgspec.Struct):
    path: str
    type: Literal["docker", "pip", "npm"]


class Outdated(Enum):
    UNKNOWN = -1
    NO = 0
    MAYBE = 1
    ALMOST = 2
    YES = 3


class Dependency(msgspec.Struct):
    entry: DepFileEntry
    value: str
    outdated: Outdated = Outdated.UNKNOWN


class RepoBranchDeps(msgspec.Struct):
    repo: RepoToCheck
    branch: str
    dependencies: list[Dependency]
