import github3
import msgspec
from termcolor import cprint

from spruce.serializers import load_json, save_json


class RepoToCheck(msgspec.Struct):
    name: str
    created_at: str
    pushed_at: str
    default_branch: str
    check_branches: list[str]


def update_repos(
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
    g: github3.GitHub,
    organization: str,
    pushed_after: str | None = None,
    force_update: bool = False,
) -> list[RepoToCheck]:
    # try loading from file if it exists and force_update is false
    cached_repos = load_json("out/repositories.json", type=list[RepoToCheck])
    if not force_update and cached_repos:
        return cached_repos

    # fetch from github api if not in cache
    repo_iter = g.organization(organization).repositories()
    repos = []

    for repo in repo_iter:
        if repo.archived:
            continue
        if pushed_after and repo.pushed_at < pushed_after:
            continue

        repos.append(
            RepoToCheck(
                name=repo.full_name,
                created_at=repo.created_at,
                pushed_at=repo.pushed_at,
                default_branch=repo.default_branch,
                check_branches=[repo.default_branch],
            )
        )

    repos.sort(key=lambda r: r.created_at, reverse=True)

    if cached_repos:
        repos = update_repos(repos, cached_repos)

    save_json(repos, "out/repositories.json")

    return repos


# def check_repositories(g, organization: str, created_after=None, pushed_after=None):
#     repos = g.organization(organization).repositories()

#     results = []

#     for repo in repos:
#         if repo.archived:
#             continue
#         if created_after and repo.created_at < created_after:
#             continue
#         if pushed_after and repo.pushed_at < pushed_after:
#             continue
#         ref = repo.default_branch

#         result = {
#             "repo": repo.full_name,
#             "created_at": repo.created_at,
#             "last_push": repo.pushed_at,
#             "ref": ref,
#             "versions": {},
#         }
#         results.append(result)

#         print("Checking " + repo.full_name)
#         print(f" > created at: {repo.created_at}")
#         print(f" > last push:  {repo.pushed_at}")
#         print(f" > ref:        {ref}")

#         tree = repo.tree(ref, recursive=True)
#         deps = find_dependency_files(tree)
#         if "docker" in deps:
#             result["versions"]["docker"] = check_docker(repo, ref, deps["docker"])
#         if "pip" in deps:
#             result["versions"]["pip"] = check_pip(repo, ref, deps["pip"])
#         if "npm" in deps:
#             result["versions"]["npm"] = check_npm(repo, ref, deps["npm"])

#     print(results)
#     json.dump(results, open("results.json", "w"), indent=2)
