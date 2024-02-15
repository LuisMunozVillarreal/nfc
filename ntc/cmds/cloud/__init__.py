import click

from .install import install as install_cmd
from .uninstall import uninstall as uninstall_cmd
from .purge import purge as purge_cmd
from .reinstall import reinstall as reinstall_cmd
from .upgrade import upgrade as upgrade_cmd

from ..kubectl import kubectl as kubectl_cmd
from ..kubectl import use_context as use_context_cmd


@click.group()
@click.pass_context
def cloud(ctx, **kwargs):
    ctx.forward(kubectl_cmd)
    ctx.forward(use_context_cmd)


cloud.add_command(install_cmd)
cloud.add_command(uninstall_cmd)
cloud.add_command(purge_cmd)
cloud.add_command(reinstall_cmd)
cloud.add_command(upgrade_cmd)
