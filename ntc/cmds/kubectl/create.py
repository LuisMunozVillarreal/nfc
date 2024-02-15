import click
import sh

from ntc.cfg import ImproperlyConfigured
from ntc.helpers.kubectl import get_namespace

from .get import namespace as get_namespace_cmd
from .get import secret as get_secret_cmd


@click.group()
def create():
    pass


@create.command()
@click.pass_context
@click.argument("name")
def namespace(ctx, name, **kwargs):
    try:
        ctx.forward(get_namespace_cmd, name=name)
        exists = True
    except sh.ErrorReturnCode_1:  # pylint: disable=no-member
        exists = False

    if exists:
        click.echo("kubectl namespace {} already exists".format(name))
        return

    args = ["create", "namespace", name]
    ctx.obj["kubectl"]["cmd"].run(args)


@create.command()
@click.pass_context
@click.argument("name")
@click.argument("content")
def secret(ctx, name, key, content, **kwargs):
    try:
        ctx.forward(get_secret_cmd, name=name)
        exists = True
    except sh.ErrorReturnCode_1:  # pylint: disable=no-member
        exists = False

    if exists:
        click.echo("kubectl secret {} already exists".format(name))
        return

    args = [
        "create", "secret", "generic", name,
        "-n", get_namespace(ctx),
        "--from-literal", "{}={}".format(key, content),
    ]
    ctx.obj["kubectl"]["cmd"].run(args)


@create.command()
@click.pass_context
@click.argument("name")
@click.argument("conf_var")
def secret_from_conf(ctx, name, key_name, conf_var, **kwargs):
    if conf_var not in ctx.obj["conf"]:
        click.echo(
            "FATAL: conf var {} not set. Secret {} can't be created".format(
                conf_var, name))
        raise ImproperlyConfigured

    ctx.forward(secret, name=name, key=key_name,
                content=ctx.obj["conf"][conf_var])
