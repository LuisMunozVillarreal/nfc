import click

from ntc.helpers.kubectl import get_namespace


@click.group()
def get():
    pass


@get.command()
@click.pass_context
@click.argument("name")
def namespace(ctx, name, **kwargs):
    args = ["get", "namespace", name]
    ctx.obj["kubectl"]["cmd"].run(args)


@get.command()
@click.pass_context
@click.argument("name")
def secret(ctx, name, **kwargs):
    args = ["get", "secret", "-n", get_namespace(ctx), name]
    ctx.obj["kubectl"]["cmd"].run(args)
