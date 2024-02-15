import click

from ntc.cfg.helm import MAIN_CHART
from ntc.helpers.kubectl import get_namespace


@click.command()
@click.pass_context
def uninstall(ctx, **kwargs):
    """helm install command.

    Args:
        ctx (dict): CLI context.
    """
    click.echo("Uninstalling {} helm chart...".format(ctx.obj["helm"]["app"]))
    args = ["uninstall", "-n", get_namespace(ctx), MAIN_CHART, "--debug"]
    ctx.obj["helm"]["cmd"].run(args)
