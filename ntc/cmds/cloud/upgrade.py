"""ntc cloud upgrade command module."""


import click
import docker as dockerpy

from ntc.cfg.apps import NUTRITION
from ntc.cfg.helm import CHART_WITH_DEPS
from ntc.cfg.tasks import CHART, IMAGE
from ntc.helpers.app import App, Nutrition

from ..docker import docker
from ..docker.build import build
from ..docker.push import push
from ..docker.tag import tag
from ..helm import helm
from ..helm.upgrade import upgrade as helm_upgrade
from ..helm.dependency import update as dep_update
from ..kubectl import kubectl, use_context


@click.command()
@click.pass_context
@click.option("--cluster")
@click.option("--set", "set_opt", multiple=True)
def upgrade(ctx, cluster, set_opt):
    """upgrade command.

    Build and upgrade the latest image to kubernetes.

    Args:
        ctx (dict): CLI context.
    """
    click.echo("Upgrade...")
    nutrition = Nutrition(ctx.obj["work_dir"], ctx.obj["env"])

    for app in ctx.obj["tasks"].keys():
        if app == NUTRITION or \
           not ctx.obj["tasks"][app][IMAGE] and \
           not ctx.obj["tasks"][app][CHART]:
            continue

        appobj = App(app, ctx.obj["work_dir"], ctx.obj["env"])
        nutrition.add_app(appobj)

        # Docker
        if ctx.obj["tasks"][app][IMAGE]:
            appobj.increase_version()
            try:
                ctx.forward(docker, app=app, tag=appobj.app_version)
                ctx.forward(build)
                ctx.forward(tag)
                ctx.forward(push)
            except dockerpy.errors.DockerException as error:
                click.echo()
                click.echo(error, err=True)
                return

        # Helm
        if ctx.obj["tasks"][app][CHART]:
            appobj.increase_chart_version()
            if app in CHART_WITH_DEPS:
                ctx.forward(helm, app=app)
                ctx.forward(dep_update)

    if ctx.obj["tasks"][NUTRITION][CHART]:
        # Update main chart
        nutrition.update_dep_versions()
        nutrition.increase_chart_version()

        # Execute upgrade
        ctx.forward(kubectl)
        ctx.forward(use_context, cluster=cluster)
        ctx.forward(helm, app=NUTRITION)
        ctx.forward(dep_update)
        ctx.forward(helm_upgrade, set_opt=set_opt)
