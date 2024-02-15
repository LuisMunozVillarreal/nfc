import click

from ..helm import helm as helm_cmd
from ..helm.uninstall import uninstall as helm_uninstall_cmd


@click.command()
@click.pass_context
def uninstall(ctx):
    ctx.forward(helm_cmd)
    ctx.forward(helm_uninstall_cmd)
