import click

from ntc.helpers.kubectl import get_namespace


@click.group()
def delete():
    pass


@delete.command()
@click.pass_context
@click.argument("name")
def secret(ctx, name, **kwargs):
    args = ["delete", "secret", "-n", get_namespace(ctx), name]
    ctx.obj["kubectl"]["cmd"].run(args)


@delete.command()
@click.pass_context
@click.argument("name")
def namespace(ctx, name, **kwargs):
    args = ["delete", "namespace", name]
    ctx.obj["kubectl"]["cmd"].run(args)
