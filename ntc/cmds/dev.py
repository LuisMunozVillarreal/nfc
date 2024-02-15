"""ntc dev command module."""


import click
import docker as dockerpy

from ntc.cfg import BASE
from ntc.cfg.apps import WEBAPP
from ntc.cfg.docker import DEV_IMGS, LATEST
from ntc.cfg.environments import DEV_ENV, PROD_ENV

from .docker import docker
from .docker.build import build
from .docker.push import push
from .docker.start import start
from .docker.tag import tag as tag_cmd


@click.group()
@click.pass_context
@click.option("--app", default=WEBAPP)
def dev(ctx, app):
    """dev command."""
    if app not in DEV_IMGS:
        click.echo("{} doesn't have a development image".format(app))
        return

    ctx.obj["env"] = DEV_ENV
    ctx.obj["dev"] = {
        "app": app,
    }


@dev.command()
@click.pass_context
@click.option("--tag")
@click.option("--base", is_flag=True)
def create_image(ctx, tag, base):
    """create image command.

    Args:
        ctx (dict): CLI context.
        tag (str): image tag.
    """
    app = ctx.obj["dev"]["app"]

    click.echo("Create new {} development image...".format(app))

    img_type = None
    if base:
        img_type = BASE

    ctx.forward(docker, app=app, tag=tag, img_type=img_type)
    ctx.forward(build)

    # Given tag
    ctx.forward(tag_cmd)
    ctx.forward(push)

    # Latest tag
    ctx.forward(docker, app=app, tag=LATEST, img_type=img_type)
    ctx.forward(tag_cmd)
    ctx.forward(push)


@dev.command()
@click.pass_context
def shell(ctx):
    """dev shell commmand.

    Opens a shell on the latest webapp dev image.

    Args:
        ctx (dict): CLI context.
    """
    app = ctx.obj["dev"]["app"]
    click.echo("{} development server shell...".format(app))
    ctx.forward(docker, app=app)
    ctx.forward(start)


@dev.command(name="start")
@click.pass_context
@click.option("--prod-img", is_flag=True)
def start_server(ctx, prod_img):
    """dev start command.

    Starts the latest webapp docker image.

    Args:
        ctx (dict): CLI context.
        prod_img (bool): flag to use a prod image instead of dev one.
    """
    app = ctx.obj["dev"]["app"]

    if prod_img:
        click.echo("Starting {} production image locally...".format(app))
        tag = None
        ctx.obj["env"] = PROD_ENV
    else:
        click.echo("Starting {} development server...".format(app))
        tag = LATEST

    ctx.forward(docker, app=app, tag=tag)
    if prod_img:
        try:
            ctx.forward(build)
        except dockerpy.errors.DockerException as error:
            click.echo()
            click.echo(error, err=True)
            return

    ctx.forward(start, command=None)
