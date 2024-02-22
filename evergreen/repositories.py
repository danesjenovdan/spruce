import json

from .dependency_checkers.docker import check as check_docker
from .dependency_checkers.npm import check as check_npm
from .dependency_checkers.pip import check as check_pip
from .find_dependency_files import find_dependency_files


def check_repositories(g, organization: str, created_after=None, pushed_after=None):
    repos = g.organization(organization).repositories()

    results = []

    for repo in repos:
        if repo.archived:
            continue
        if created_after and repo.created_at < created_after:
            continue
        if pushed_after and repo.pushed_at < pushed_after:
            continue
        ref = repo.default_branch

        result = {
            "repo": repo.full_name,
            "created_at": repo.created_at,
            "last_push": repo.pushed_at,
            "ref": ref,
            "versions": {},
        }
        results.append(result)

        print("Checking " + repo.full_name)
        print(f" > created at: {repo.created_at}")
        print(f" > last push:  {repo.pushed_at}")
        print(f" > ref:        {ref}")

        tree = repo.tree(ref, recursive=True)
        deps = find_dependency_files(tree)
        if "docker" in deps:
            result["versions"]["docker"] = check_docker(repo, ref, deps["docker"])
        if "pip" in deps:
            result["versions"]["pip"] = check_pip(repo, ref, deps["pip"])
        if "npm" in deps:
            result["versions"]["npm"] = check_npm(repo, ref, deps["npm"])

    print(results)
    json.dump(results, open("results.json", "w"), indent=2)
