"""ntc command package."""


import click


from .cfg.apps import APPS
from .cfg.environments import PROD_ENV, STAGING_ENV
from .cmds.app import app
from .cmds.docker import docker
from .cmds.helm import helm
from .helpers.workdir import get_work_dir


@click.group()
@click.pass_context
@click.option(
    "-e", "--env", default=STAGING_ENV, type=click.Choice(
        [STAGING_ENV, PROD_ENV], case_sensitive=False)
)
@click.option(
    "-a", "--apps", default=["backend"], type=click.Choice(
        APPS, case_sensitive=False), multiple=True,
)
@click.option("-v", "--debug", is_flag=True)
def nutrition_cli(ctx, env, apps, debug):
    """Nutrition CLI.

    Args:
        ctx (dict): CLI context.
        env (str): environemnt to work on.
        apps (List): apps to action on.
        debug (bool): debug mode.
    """
    ctx.obj = {
        "work_dir": get_work_dir(),
        "env": env,
        "apps": apps,
        "debug": debug,
    }


nutrition_cli.add_command(app)
nutrition_cli.add_command(docker)
nutrition_cli.add_command(helm)
