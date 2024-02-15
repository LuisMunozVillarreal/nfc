"""ntc dev command module."""


import click

from ntc.helpers.app import App, Nutrition

from .helm import helm
from .helm.dependency import update as dep_update


@click.group()
def app():
    """app command."""


@app.command()
@click.pass_context
@click.option("--fix", is_flag=True, default=False)
def increase_version(ctx, fix):
    """increase-version command.

    Increase versions to apps and charts.

    Args:
        ctx (dict): CLI context.
    """
    click.echo("Increasing versions...")
    nutrition = Nutrition(ctx.obj["work_dir"])

    for app in ctx.obj["apps"]:
        appobj = App(app, ctx.obj["work_dir"])
        nutrition.add_app(appobj)

        appobj.increase_version(False, fix)
        appobj.increase_chart_version(False)

    # Update main chart
    nutrition.update_dep_versions()
    nutrition.increase_chart_version(False)

