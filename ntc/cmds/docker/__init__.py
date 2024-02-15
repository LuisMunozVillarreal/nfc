"""ntc docker command package."""


import os

import click
import docker as dockerpy

from ntc.cfg import BASE, DEV
from ntc.cfg.apps import WEBAPP
from ntc.cfg.docker import DOCKER_DIR, DOCKERFILE, REGISTRY
from ntc.cfg.environments import DEV_ENV
from ntc.helpers.tag import generate_tag

from .build import build as build_cmd
from .push import push as push_cmd
from .start import start as start_cmd
from .tag import tag as tag_cmd


@click.group()
@click.pass_context
@click.option("--app", default=WEBAPP)
@click.option("--tag", help="This option is mainly used for dev images.")
@click.option("--registry", default=REGISTRY)
@click.option("--img-type")
def docker(ctx, app, tag, registry, img_type, **kwargs):
    # pylint: disable=unused-argument
    """docker command.

    Args:
        ctx (dict): CLI context.
        app (str): app to be built.
        registry (str): docker registry to be used
        kwargs (dict): named arguments
    """
    if not tag:
        tag = generate_tag(ctx.obj["work_dir"], app)

    img_name = app
    dockerfile = DOCKERFILE
    if img_type == BASE:
        img_name = "{}-{}".format(app, img_type)
        dockerfile = "{}.{}".format(DOCKERFILE, img_type)
    elif ctx.obj["env"] == DEV_ENV:
        img_name = "{}-{}".format(app, DEV)
        dockerfile = "{}.{}".format(DOCKERFILE, DEV)

    ctx.obj["docker"] = {
        "lib": dockerpy.from_env(),
        "registry": registry,
        "app": {
            "name": img_name,
            "repository": {
                "name": img_name,
                "path": os.path.join(registry, img_name),
            },
            "build_context": os.path.join(ctx.obj["work_dir"], app),
            "dockerfile": os.path.join(DOCKER_DIR, dockerfile),
            "image": {
                "name": "{}:{}".format(img_name, tag),
                "latest": "{}:{}".format(img_name, "latest"),
                "tag": tag,
            },
        },
    }


docker.add_command(build_cmd)
docker.add_command(tag_cmd)
docker.add_command(push_cmd)
docker.add_command(start_cmd)
