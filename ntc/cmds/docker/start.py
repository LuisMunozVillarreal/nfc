"""ntc docker start command module."""


import os

import click
import docker as dockerpy
import dockerpty

from ntc.cfg.apps import API, WEBAPP
from ntc.cfg.docker import ASH, BASH, DOCKER_DIR, ENV_FILE, POSTGRES_DATA_DIR


def _env_variables(path):
    """Read env variables from the .env file.

    Args:
        path (str): path to the .env file.

    Returns:
        list: the env variables.
    """
    try:
        with open(path) as dotenv:
            return dotenv.read().splitlines()
    except FileNotFoundError:
        click.echo("ERROR: .env file {} doesn't exist".format(path))


@click.command()
@click.pass_context
@click.option("--command", default=ASH)
def start(ctx, command, **kwargs):
    # pylint: disable=unused-argument
    """docker start command.

    Args:
        ctx (dict): CLI context.
        command (str): command to be executed on the container.
        kwargs (dict): named arguments.
    """
    app = ctx.obj["docker"]["app"]

    click.echo("Starting {} docker image...".format(app["name"]))

    image = app["image"]["name"]
    if "prod_img" not in kwargs:
        image = app["image"]["latest"]

    # API
    env_vars = _env_variables(os.path.join(
        ctx.obj["work_dir"], API, ENV_FILE))
    command = BASH
    volumes = {
        "nutrition_db": {
            "bind": POSTGRES_DATA_DIR, "mode": "rw",
        },
        "{}/{}".format(ctx.obj["work_dir"], API): {
            "bind": "/srv/www/{}".format(API), "mode": "rw",
        },
        "api_home": {
            "bind": "/home/api", "mode": "rw",
        },
    }
    ports = {"8000/tcp": "8000"}
    name = "api-dev"

    # WebApp
    if WEBAPP in app["name"]:
        env_vars = _env_variables(os.path.join(
            ctx.obj["work_dir"], WEBAPP, ENV_FILE))
        volumes = {
            "{}/{}".format(ctx.obj["work_dir"], WEBAPP): {
                "bind": "/p", "mode": "rw",
            },
            "webapp_home": {
                "bind": "/home/node", "mode": "rw",
            },
        }
        command = ASH
        ports = {"3000/tcp": "3000", "9229/tcp": "9229"}
        name = "webapp-dev"

    tty = True

    if ctx.obj["debug"]:
        msg = "debug: executed cmd: docker run" \
            "{tty} {volumes} {ports} {image} {cmd}"
        tty_msg = " -t" if tty else ""
        vols_msg = " ".join(
            ["-v {}:{}".format(key, volumes[key]["bind"]) for key in volumes])
        ports_msg = " ".join(
            ["-p {}:{}".format(key, ports[key]) for key in ports])
        click.echo(msg.format(tty=tty_msg, volumes=vols_msg, ports=ports_msg,
                              image=image, cmd=command))

    container = ctx.obj["docker"]["lib"].containers.create(
        image,
        command=command,
        ports=ports,
        tty=tty,
        stdin_open=True,
        volumes=volumes,
        environment=env_vars,
        name=name,
    )

    try:
        dockerpty.start(ctx.obj["docker"]["lib"].api, container.id)
    except dockerpy.errors.APIError as error:
        click.echo(error)

    click.echo("Removing container...")
    container.remove()
