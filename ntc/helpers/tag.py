import time

import git


def generate_tag(work_dir, app):
    """Generate tag for docker iamges.
    Args:
        work_dir (str): Work directory
        env (str): environemnt
    Returns:
        str: tag
    """
    repo = git.Repo(work_dir)
    tag = repo.head.object.hexsha[:7]

    tag = "{}-{}".format(tag, int(time.time()))

    return tag
