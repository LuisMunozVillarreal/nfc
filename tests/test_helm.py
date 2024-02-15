"""Tests for ntc helm command."""


from tests import assert_exit_code
from ntc import nutrition_cli
from ntc.cfg.helm import CHARTS_PATH, PRODUCTION_VALUES_FILE
from ntc.cfg.namespaces import PROD_NAMESPACE


def _update_helper(runner, open_dev_app_chart, cmd, app):
    """Test helper for update-app-version tests."""
    result = runner.invoke(nutrition_cli, cmd)
    assert_exit_code(result, 0)
    open_dev_app_chart.assert_called_once()
    assert "kube/{}".format(app) in open_dev_app_chart.call_args.args[0]


def _upgrade_helper(runner, sh, cmd, app, namespace="staging"):
    # pylint: disable=too-many-arguments
    """Test helper for upgrade tests."""
    result = runner.invoke(nutrition_cli, cmd)
    assert_exit_code(result, 0)
    sh.assert_called_once()
    sh.return_value.assert_called_once()
    args = sh.return_value.call_args.args
    assert args[1] == app
    assert CHARTS_PATH in args[2]
    assert args[4] == namespace
    if namespace == PROD_NAMESPACE:
        assert args[6] == "-f"
        assert PRODUCTION_VALUES_FILE in args[7]
        assert len(PRODUCTION_VALUES_FILE) < len(args[7])


def test_helm_upgrade(runner, sh):
    """Test ntc helm upgrade command."""
    cmd = ["helm", "upgrade"]
    _upgrade_helper(runner, sh, cmd, "nutrition")


def test_helm_upgrade_reverse_proxy(runner, sh):
    """Test ntc helm upgrade command."""
    cmd = ["-t", "reverse-proxy.chart", "helm", "upgrade"]
    _upgrade_helper(runner, sh, cmd, "nutrition")


def test_helm_upgrade_production(runner, sh):
    """Test ntc helm upgrade command."""
    cmd = ["-e", "production", "helm", "upgrade"]
    _upgrade_helper(runner, sh, cmd, "nutrition", namespace="production")
