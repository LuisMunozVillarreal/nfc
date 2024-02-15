import os

import click

from .kubectl import get_namespace

from ..cfg import ImproperlyConfigured
from ..cfg.environments import PROD_ENV
from ..cfg.helm import CHARTS_PATH, POSTGRESQL_PASSWORD_CONF_VAR


def get_set_opts(ctx):
    if POSTGRESQL_PASSWORD_CONF_VAR not in ctx.obj["conf"]:
        click.echo(
            "FATAL: env var {} not set. --set options can't be generated"
            .format(POSTGRESQL_PASSWORD_CONF_VAR))
        raise ImproperlyConfigured()

    set_opts = ["--set", "api.postgresql.postgresqlPassword={}".format(
        ctx.obj["conf"][POSTGRESQL_PASSWORD_CONF_VAR])]

    if ctx.obj["env"] == PROD_ENV:
        set_opts += ["-f", os.path.join(
            ctx.obj["work_dir"], CHARTS_PATH, "production.values.yaml")]

    return set_opts
