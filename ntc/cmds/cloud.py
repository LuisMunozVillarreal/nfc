import click
import docker as dockerpy

from ntc.helpers.app import App, Nutrition
from ntc.helpers.cmd import Command

from .docker import docker
from .docker.build import build
from .docker.push import push
from .docker.tag import tag


@click.group
def cloud():
    pass


@cloud.command
@click.pass_context
def apply(ctx, **kwargs):
    nutrition = Nutrition(ctx.obj["work_dir"], ctx.obj["env"])

    for app in ctx.obj["apps"]:
        appobj = App("backend", ctx.obj["work_dir"], ctx.obj["env"])
        nutrition.add_app(appobj)

        # Docker
        appobj.increase_version()
        try:
            ctx.forward(docker, tag=appobj.app_version)
            ctx.forward(build)
            ctx.forward(tag)
            ctx.forward(push)
        except dockerpy.errors.DockerException as error:
            click.echo()
            click.echo(error, err=True)
            return

        # Helm
        appobj.increase_chart_version()

    nutrition.update_release_versions()

    # Helmfile
    Command("helmfile", ctx.obj["debug"]).run(["apply"])
