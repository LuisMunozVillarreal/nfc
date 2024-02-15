"""ntc helm command package."""


import os

import click

from ntc.cfg.apps import NUTRITION, WEBAPP
from ntc.cfg.helm import CHARTS_PATH
from ntc.helpers.cmd import Command
from ntc.helpers.kubectl import get_namespace

from .dependency import dependency as dependency_cmd


@click.group()
@click.pass_context
@click.option("--app", default=WEBAPP)
def helm(ctx, app, **kwargs):
    # pylint: disable=unused-argument
    """helm command.

    Args:
        ctx (dict): CLI context.
        app (str): app to be built.
        kwargs (dict): named arguments
    """
    chart_path = os.path.join(ctx.obj["work_dir"], app, CHARTS_PATH)
    if app == NUTRITION:
        chart_path = os.path.join(ctx.obj["work_dir"], CHARTS_PATH)

    ctx.obj["helm"] = {
        "app": app,
        "chart": {
            "path": chart_path,
        },
        "cmd": Command("helm", ctx.obj["debug"]),
        "namespace": get_namespace(ctx),
    }


helm.add_command(dependency_cmd)
