from os.path import dirname, join

import click
from dotenv import load_dotenv

from spruce.github_auth import github_login
from spruce.repositories import check_repos_versions, list_repos

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


@click.group()
def cli() -> None:
    pass


@click.command()
@click.option(
    "--force-update",
    is_flag=True,
    help="Force re-fetching repositories from GitHub.",
)
def list_repositories(force_update: bool) -> None:
    g = github_login()
    list_repos(g, "danesjenovdan", pushed_after="2020-01-01", force_update=force_update)


@click.command()
def check_versions() -> None:
    g = github_login()
    check_repos_versions(g)


cli.add_command(list_repositories)
cli.add_command(check_versions)


if __name__ == "__main__":
    cli()
