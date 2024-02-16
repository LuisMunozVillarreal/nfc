"""ntc docker tag command module."""

import os

import click


@click.command()
@click.pass_context
def tag(ctx, **kwargs):
    # pylint: disable=unused-argument
    """docker tag command.

    Args:
        ctx (dict): CLI context.
        kwargs (dict): named arguments
    """
    app = ctx.obj["docker"]["app"]

    click.echo("Tagging {} docker image...".format(app["name"]))

    img = ctx.obj["docker"]["lib"].images.get(app["image"]["name"])
    res = img.tag(
        os.path.join(ctx.obj["docker"]["registry"], app["image"]["name"])
    )

    if res:
        click.echo("Tagged with {}".format(app["image"]["name"]))
    else:
        click.echo("Error: not tagged")
