import click

from .install import install as cloud_install_cmd
from .purge import purge as cloud_purge_cmd
from .uninstall import uninstall as cloud_uninstall_cmd


@click.command()
@click.pass_context
@click.option("--no-purge", is_flag=True, default=False)
def reinstall(ctx, no_purge, **kwargs):
    if no_purge:
        try:
            ctx.forward(cloud_uninstall_cmd)
        except sh.ErrorReturnCode_1:  # pylint: disable=no-member
            pass
    else:
        ctx.forward(cloud_purge_cmd)

    ctx.forward(cloud_install_cmd)
