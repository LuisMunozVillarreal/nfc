import os

import git


def get_work_dir():
    git_repo = git.Repo(".", search_parent_directories=True)
    return git_repo.git.rev_parse("--show-toplevel")
