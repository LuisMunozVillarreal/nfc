"""ntc docker build command module."""

import os

import click
import docker as dockerpy

from ntc.cfg.apps import BACKEND
from ntc.cfg.docker import DOCKERFILE
from ntc.cfg.environments import PROD_ENV, STAGING_ENV


@click.command()
@click.pass_context
@click.option("-f", "--dockerfile")
def build(ctx, dockerfile, **kwargs):
    # pylint: disable=unused-argument
    """docker build command.

    Args:
        ctx (dict): CLI context.
        dockerfile (str): dockerfile to be used.
        kwargs (dict): named arguments.

    Raises:
        DockerException: if the build fails
    """
    app = ctx.obj["docker"]["app"]
    click.echo("Building {} docker image...".format(app["name"]))

    if not dockerfile:
        dockerfile = DOCKERFILE

    build_args = {"ENV": STAGING_ENV}
    if ctx.obj["env"] == PROD_ENV:
        build_args = {"ENV": PROD_ENV}

    generator = ctx.obj["docker"]["lib"].api.build(
        path=app["build_context"],
        dockerfile=app["dockerfile"],
        tag=app["image"]["name"],
        decode=True,
        buildargs=build_args,
    )

    success = True
    error = None
    for line in generator:
        if "stream" in line:
            line = line["stream"]
        elif "errorDetail" in line:
            error = line["errorDetail"]
            success = False

        click.echo(line, nl=False)

    if success:
        img = ctx.obj["docker"]["lib"].images.get(app["image"]["name"])
        img.tag(app["image"]["latest"])
    else:
        raise dockerpy.errors.DockerException(
            "Docker build failed\n{}".format(error)
        )
