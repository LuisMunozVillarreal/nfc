"""ntc dev command module."""


import click

from ntc.cfg.apps import NUTRITION
from ntc.cfg.helm import CHART_WITH_DEPS
from ntc.cfg.tasks import CHART, IMAGE
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

    for app in ctx.obj["tasks"].keys():
        if app == NUTRITION or \
           not ctx.obj["tasks"][app][IMAGE] and \
           not ctx.obj["tasks"][app][CHART]:
            continue

        appobj = App(app, ctx.obj["work_dir"])
        nutrition.add_app(appobj)

        # App version
        if ctx.obj["tasks"][app][IMAGE]:
            appobj.increase_version(False, fix)

        # Helm version
        if ctx.obj["tasks"][app][CHART]:
            appobj.increase_chart_version(False)
            if app in CHART_WITH_DEPS:
                ctx.forward(helm, app=app)
                ctx.forward(dep_update)

    if ctx.obj["tasks"][NUTRITION][CHART]:
        # Update main chart
        nutrition.update_dep_versions()
        nutrition.increase_chart_version(False)
        ctx.forward(helm, app=NUTRITION)
        ctx.forward(dep_update)
