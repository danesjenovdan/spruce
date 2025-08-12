from click import ClickException
from github3 import GitHub
from github3.git import Tree
from github3.orgs import Organization
from github3.repos import Repository
from termcolor import cprint

from .dependency_checkers.docker import check as check_docker
from .find_dependency_files import find_dependency_files
from .serializers import load_json, save_json
from .structs import Dependency, RepoBranchDeps, RepoToCheck


def _update_repos_with_cache(
    repos: list[RepoToCheck],
    cached_repos: list[RepoToCheck],
) -> list[RepoToCheck]:
    for repo in repos:
        cached_repo = next((r for r in cached_repos if r.name == repo.name), None)
        if cached_repo:
            if cached_repo.default_branch != repo.default_branch:
                cprint(f"WARNING: {repo.name} default branch changed!", "yellow")
            repo.check_branches = cached_repo.check_branches
    return repos


def list_repos(
    g: GitHub,
    organization: str,
    pushed_after: str | None = None,
    force_update: bool = False,
) -> list[RepoToCheck]:
    # try loading from file if it exists and force_update is false
    cached_repos = load_json("out/repositories.json", type=list[RepoToCheck])
    if not force_update and cached_repos:
        cprint(
            f"INFO: Using {len(cached_repos)} cached repositories! "
            "See `out/repositories.json` for details.",
            "cyan",
        )
        return cached_repos

    # fetch from github api if not in cache
    org: Organization = g.organization(organization)
    repo_iter = org.repositories()
    repos = []

    repo: Repository
    for repo in repo_iter:
        if repo.archived:
            continue
        if pushed_after and repo.pushed_at < pushed_after:
            continue

        repos.append(
            RepoToCheck(
                owner=repo.owner.login,
                name=repo.name,
                created_at=repo.created_at,
                pushed_at=repo.pushed_at,
                default_branch=repo.default_branch,
                check_branches=[repo.default_branch],
            )
        )

    repos.sort(key=lambda r: r.created_at, reverse=True)

    if cached_repos:
        repos = _update_repos_with_cache(repos, cached_repos)

    save_json(repos, "out/repositories.json")

    cprint(
        f"INFO: Updated list of {len(repos)} repositories! "
        "See `out/repositories.json` for details.",
        "cyan",
    )

    return repos


# TODO: clean up this function
def _find_named_deps_string(deps: list[Dependency], name: str) -> str:
    return ";".join([dep.value for dep in deps if name in dep.value])


def check_repos_versions(g: GitHub) -> None:
    repos = load_json("out/repositories.json", type=list[RepoToCheck])
    if not repos:
        cprint(
            "ERROR: Could not read repositories file. "
            "Make sure to run `list-repositories` command first.",
            "red",
        )
        raise ClickException("Could not read repositories file.")

    with open("out/repository_branch_dependencies.csv", "w") as f:
        f.write("owner,name,branch,python,node,postgresql,nginx,solr\n")

    count = len(repos)
    count_width = len(str(count))

    for i, repo in enumerate(repos):
        print(f"Checking repository {i + 1:>{count_width}}/{count} {repo.name} ...")
        repository: Repository = g.repository(repo.owner, repo.name)

        for ref in repo.check_branches:
            deps = []

            tree: Tree = repository.tree(ref, recursive=True)
            deps_entries = find_dependency_files(tree)

            for dep_entry in deps_entries:
                if dep_entry.type == "docker":
                    deps += check_docker(repository, ref, dep_entry)
                # TODO: check pip and npm

            rbd = RepoBranchDeps(repo=repo, branch=ref, dependencies=deps)

            with open("out/repository_branch_dependencies.csv", "a") as f:
                f.write(f"{rbd.repo.owner},{rbd.repo.name},{rbd.branch},")
                f.write(f"{_find_named_deps_string(rbd.dependencies, 'python')},")
                f.write(f"{_find_named_deps_string(rbd.dependencies, 'node')},")
                f.write(f"{_find_named_deps_string(rbd.dependencies, 'postgres')},")
                f.write(f"{_find_named_deps_string(rbd.dependencies, 'nginx')},")
                f.write(f"{_find_named_deps_string(rbd.dependencies, 'solr')}\n")
