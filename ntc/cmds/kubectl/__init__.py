"""ntc kubectl command package."""


import os
import sys

import click

from ntc.cfg.contexts import PROD_CONTEXT, STAGING_CONTEXT
from ntc.cfg.environments import PROD_ENV
from ntc.helpers.cmd import Command

from .create import create as create_cmd
from .delete import delete as delete_cmd
from .get import get as get_cmd


@click.group()
@click.pass_context
def kubectl(ctx, **kwargs):
    """ntc kubectl command."""
    ctx.obj["kubectl"] = {
        "cmd": Command("kubectl", ctx.obj["debug"]),
    }


@kubectl.command(name="use-context")
@click.pass_context
@click.option("--cluster")
def use_context(ctx, cluster, **kwargs):
    """ntc kubectl use-context command.

    Args:
        ctx (dict): CLI context.
    """
    context = STAGING_CONTEXT
    if cluster:
        if cluster == PROD_ENV:
            context = PROD_CONTEXT
    elif ctx.obj["env"] == PROD_ENV:
        context = PROD_CONTEXT

    click.echo("Using {} context...".format(context))

    args = ["config", "use-context", context]
    ctx.obj["kubectl"]["cmd"].run(args)


kubectl.add_command(create_cmd)
kubectl.add_command(delete_cmd)
kubectl.add_command(get_cmd)
