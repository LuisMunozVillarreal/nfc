"""ntc helm dependency command module."""


import os
import sys

import click


@click.group()
def dependency():
    pass

@dependency.command()
@click.pass_context
def update(ctx, **kwargs):
    """helm dependency update command.

    Args:
        ctx (dict): CLI context.
    """
    click.echo("Updating {} helm chart dependencies...".format(
        ctx.obj["helm"]["app"]))
    args = ["dependency", "update", "--debug", "--skip-refresh"]
    ctx.obj["helm"]["cmd"].run(
        args, {"_cwd": ctx.obj["helm"]["chart"]["path"]})
