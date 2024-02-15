import click

from ntc.cfg.helm import MAIN_CHART
from ntc.helpers.helm import get_set_opts
from ntc.helpers.kubectl import get_namespace


@click.command()
@click.pass_context
def install(ctx, **kwargs):
    """helm install command.

    Args:
        ctx (dict): CLI context.
    """
    click.echo("Installing {} helm chart...".format(ctx.obj["helm"]["app"]))
    args = ["install", "-n", get_namespace(ctx),
            MAIN_CHART, ctx.obj["helm"]["chart"]["path"], "--debug"]
    args += get_set_opts(ctx)
    ctx.obj["helm"]["cmd"].run(args)
