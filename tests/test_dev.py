"""Tests for ntc dev command."""


from tests import assert_exit_code
from ntc import nutrition_cli


def test_dev_create_image(runner, dockerobj):
    """Test ntc dev shell command."""
    result = runner.invoke(nutrition_cli, ["dev", "create-image", "--tag", "t"])
    assert_exit_code(result, 0)
    assert dockerobj.call_count == 2

    assert "Building" in result.output
    dockerobj.return_value.api.build.assert_called_once()

    assert "Tagging" in result.output
    assert dockerobj.return_value.images.get.call_count == 3

    assert "Pushing" in result.output
    assert dockerobj.return_value.images.push.call_count == 2


def test_dev_shell(runner, dockerobj, dockerpty, open_env):
    """Test ntc dev shell command."""
    result = runner.invoke(nutrition_cli, ["dev", "shell"])
    args = dockerobj.return_value.containers.create.call_args.args
    assert "webapp-dev" in args[0]
    assert_exit_code(result, 0)


def test_dev_start(runner, dockerobj, dockerpty, open_env):
    """Test ntc dev start command."""
    result = runner.invoke(nutrition_cli, ["dev", "start"])
    assert_exit_code(result, 0)


def test_dev_start_prod_img(runner, dockerobj, dockerpty, open_env):
    """Test ntc dev start command with --prod-img flag."""
    result = runner.invoke(nutrition_cli, ["dev", "start", "--prod-img"])
    assert_exit_code(result, 0)
    assert "locally" in result.output


def test_dev_start_prod_img_build_error(
        runner, dockerobj, dockerpty, open_env):
    """Test ntc dev start command with --prod-img flag and build faling."""
    dockerobj.return_value.api.build.return_value = [
        {"errorDetail": "hola"}
    ]
    result = runner.invoke(nutrition_cli, ["dev", "start", "--prod-img"])
    assert_exit_code(result, 0)
    assert "locally" in result.output
    assert "Docker start" not in result.output
