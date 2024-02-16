"""ntc docker push command module."""

import click
import docker as dockerpy


@click.command()
@click.pass_context
def push(ctx, **kwargs):
    # pylint: disable=unused-argument
    """docker push command.

    Args:
        ctx (dict): CLI context.
        kwargs (dict): named arguments

    Raises:
        DockerException: if the build fails
    """
    app = ctx.obj["docker"]["app"]

    click.echo(
        "Pushing {} docker image to {}...".format(
            app["name"], app["repository"]["path"]
        )
    )

    success = True
    error = None
    for line in ctx.obj["docker"]["lib"].images.push(
        app["repository"]["path"],
        tag=app["image"]["tag"],
        stream=True,
        decode=True,
    ):
        if "stream" in line:
            line = line["status"]
        elif "errorDetail" in line:
            error = line["errorDetail"]
            success = False

        click.echo(line)

    if not success:
        raise dockerpy.errors.DockerException(
            "Docker push failed\n{}".format(error)
        )
