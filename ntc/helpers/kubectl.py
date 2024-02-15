from ntc.cfg.environments import PROD_ENV
from ntc.cfg.namespaces import PROD_NAMESPACE, STAGING_NAMESPACE


def get_namespace(ctx):
    namespace = STAGING_NAMESPACE
    if ctx.obj["env"] == PROD_ENV:
        namespace = PROD_NAMESPACE
    return namespace
