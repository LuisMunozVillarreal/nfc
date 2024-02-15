"""Tests for ntc cloud upgrade command."""


from tests import assert_exit_code
from ntc import nutrition_cli


def test_upgrade(runner, dockerobj, dockerpty, open_dev_main_chart, sh):
    """Test ntc cloud upgrade command."""
    result = runner.invoke(nutrition_cli, ["cloud", "upgrade"])
    assert_exit_code(result, 0)


def test_upgrade_build_error(
        runner, dockerobj, dockerpty, open_dev_app_chart, sh):
    """Test ntc cloud upgrade command when build command throws an error."""
    dockerobj.return_value.api.build.return_value = [
        {"errorDetail": "hola"}
    ]
    result = runner.invoke(nutrition_cli, ["cloud", "upgrade"])
    assert_exit_code(result, 0)
