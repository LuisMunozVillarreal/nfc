"""ntc helm upgrade command module."""


import os
import sys

import click
import sh

from ntc.cfg.helm import MAIN_CHART, PRODUCTION_VALUES_FILE
from ntc.cfg.namespaces import PROD_NAMESPACE
from ntc.helpers.helm import get_set_opts


@click.command()
@click.pass_context
@click.option("--set", "set_opt", multiple=True)
def upgrade(ctx, set_opt, **kwargs):
    """helm upgrade command.

    Args:
        ctx (dict): CLI context.
        kwargs (dict): named arguments.
    """
    click.echo("Upgrading {} helm chart on {} namespace...".format(
        ctx.obj["helm"]["app"], ctx.obj["helm"]["namespace"]))

    set_opts = []
    if set_opt:
        for opt in set_opt:
            set_opts += ["--set", opt]
    set_opts += get_set_opts(ctx)

    args = ["upgrade", MAIN_CHART, ctx.obj["helm"]["chart"]["path"],
            "--namespace", ctx.obj["helm"]["namespace"], "--debug"] + set_opts

    if ctx.obj["helm"]["namespace"] == PROD_NAMESPACE:
        prod_values_file = os.path.join(
            ctx.obj["helm"]["chart"]["path"], PRODUCTION_VALUES_FILE)
        args.extend(["-f", prod_values_file])

    ctx.obj["helm"]["cmd"].run(args)
