"""ntc command package."""


import click


from .cfg.environments import DEV_ENV, PROD_ENV, STAGING_ENV
from .cfg.tasks import TASKS_STRS
from .cmds.app import app
from .cmds.docker import docker
from .cmds.helm import helm
from .helpers.tasks import computed_tasks
from .helpers.config import NtcConfig


@click.group()
@click.pass_context
@click.option("-e", "--env", default=STAGING_ENV, type=click.Choice(
    [DEV_ENV, STAGING_ENV, PROD_ENV], case_sensitive=False))
@click.option("-t", "--tasks", default=["webapp.all"], type=click.Choice(
    TASKS_STRS, case_sensitive=False), multiple=True)
@click.option("-v", "--debug", is_flag=True)
def nutrition_cli(ctx, env, tasks, debug):
    """Nutrition CLI.

    Args:
        ctx (dict): CLI context.
        env (str): environemnt to work on.
        tasks (str): tasks to execute.
        debug (bool): debug mode.
    """
    config = NtcConfig()

    ctx.obj = {
        "work_dir": config["DEFAULT"]["WorkDir"],
        "env": env,
        "tasks": computed_tasks(tasks),
        "debug": debug,
    }


nutrition_cli.add_command(app)
nutrition_cli.add_command(docker)
nutrition_cli.add_command(helm)
