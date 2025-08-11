from os.path import dirname, join

import click
from dotenv import load_dotenv

from spruce.github_auth import github_login
from spruce.repositories import check_repos, list_repos

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


@click.group()
def cli() -> None:
    pass


@click.command()
@click.option(
    "--force",
    is_flag=True,
    help="Force re-fetching repositories from GitHub.",
)
def list_repositories(force: bool) -> None:
    g = github_login()
    list_repos(g, "danesjenovdan", pushed_after="2020-01-01", force_update=force)


@click.command()
def check_repositories() -> None:
    g = github_login()
    check_repos(g)


cli.add_command(list_repositories)
cli.add_command(check_repositories)


if __name__ == "__main__":
    cli()
