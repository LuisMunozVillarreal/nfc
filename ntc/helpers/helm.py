import os

import click

from .kubectl import get_namespace

from ..cfg import ImproperlyConfigured
from ..cfg.environments import PROD_ENV
from ..cfg.helm import CHARTS_PATH


def get_set_opts(ctx):
    set_opts = [
    ]

    if ctx.obj["env"] == PROD_ENV:
        set_opts += ["-f", os.path.join(
            ctx.obj["work_dir"], CHARTS_PATH, "production.values.yaml")]

    return set_opts
