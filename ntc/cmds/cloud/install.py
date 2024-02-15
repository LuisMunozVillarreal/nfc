import click
import sh

from ntc.cfg.helm import MAIN_CHART
from ntc.cfg.kubectl import KUBE_SECRETS
from ntc.cmds.helm import helm as helm_cmd
from ntc.cmds.helm.dependency import update as dep_update_cmd
from ntc.cmds.helm.install import install as helm_install_cmd
from ntc.cmds.kubectl.create import secret_from_conf as \
    create_secret_from_conf_cmd
from ntc.helpers.kubectl import get_namespace

from ..kubectl.create import namespace as create_namespace_cmd


@click.command()
@click.pass_context
def install(ctx, **kwargs):
    namespace = get_namespace(ctx)
    ctx.forward(create_namespace_cmd, name=namespace)

    for secret in KUBE_SECRETS:
        key_name = KUBE_SECRETS[secret]["key_name"]
        conf_var = KUBE_SECRETS[secret]["conf_var"]
        ctx.forward(create_secret_from_conf_cmd,
                    name=secret, key_name=key_name, conf_var=conf_var)

    ctx.forward(helm_cmd, app=MAIN_CHART)
    ctx.forward(dep_update_cmd)
    ctx.forward(helm_install_cmd)
