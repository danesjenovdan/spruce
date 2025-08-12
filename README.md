# Spruce

This is a script for checking various library versions on our project github repos.

## Prerequisites

After cloning the repo:
- create a `.env` file with a valid github token (see `.env.example`)
  - to create a token go to [your developer settings](https://github.com/settings/personal-access-tokens) and create a new fine grained token with:
    - Resource owner: `danesjenovdan`
    - Repository access: `All repositories`
    - Permissions: `Contents` and `Metadata` (both read-only)
- create a python virtual environment
- install dependencies with `pip install -r requirements.txt`

## Running the script

### Generate/update repository list

- run `./main.py list-repositories` to generate a list of repositories to check
  - by default it will use `out/repositories.json` if it exists or create it
    - you can edit the file and change the `check_branches` key for any repository if you want the script to check more branches
  - to update the list run `./main.py list-repositories --force-update`
    - this will re-fetch the repository data but leave any `check_branches` changes from the previous list

### Check versions in repositories

> [!NOTE]
> For now this script only checks for image versions in any docker and compose files!

- run `./main check-versions` to check for dependency version
  - this will generate `out/repository_branch_dependencies.csv` that will list relavant dependencies for every repository and branch


## Formatting and type checking

This project has github actions for automatic formatting and type checks

- you can use `./check_types.sh` and `./check_formatting.sh` before pushing to check for any problems
- if you use vscode you can install the recommended extensions from `.vscode/extensions.json` to assist you


## Future plans

- auto detecting if not latest version
- generate a html report
- publish report to github pages
- auto run periodically in github actions
- send report to our slack channel
- checking npm dependencies
- checking pip dependencies
