"""ntc helm command package."""


import os

import click

from ntc.cfg.apps import TRAKTION, WEBAPP
from ntc.cfg.helm import CHARTS_PATH
from ntc.helpers.cmd import Command
from ntc.helpers.kubectl import get_namespace

from .dependency import dependency as dependency_cmd
from .install import install as install_cmd
from .uninstall import uninstall as uninstall_cmd
from .upgrade import upgrade as upgrade_cmd


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
    if app == TRAKTION:
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
helm.add_command(install_cmd)
helm.add_command(uninstall_cmd)
helm.add_command(upgrade_cmd)
