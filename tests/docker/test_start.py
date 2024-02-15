"""Tests for ntc docker start command."""


import docker as dockerpy

from tests import assert_exit_code
from ntc import nutrition_cli


def _helper(result, dockerobj, dockerpty, open_env):
    """Test helper."""
    assert_exit_code(result, 0)
    assert "Starting" in result.output
    dockerobj.assert_called_once()
    dockerobj.return_value.containers.create.assert_called_once()
    dockerpty.assert_called_once()


def test_docker_start(runner, dockerobj, dockerpty, open_env):
    """Test ntc docker start command."""
    result = runner.invoke(nutrition_cli, ["-v", "docker", "start"])
    _helper(result, dockerobj, dockerpty, open_env)
    assert "3000/tcp:3000" in result.output


def test_docker_start_raise_exception(runner, dockerobj, dockerpty, open_env):
    """Test ntc docker start command when it raises an exception."""
    dockerpty.side_effect = dockerpy.errors.APIError("error")
    result = runner.invoke(nutrition_cli, ["docker", "start"])
    _helper(result, dockerobj, dockerpty, open_env)


def test_docker_start_env_file_not_found(
        runner, dockerobj, dockerpty, open_env):
    """Test ntc docker start command."""
    open_env.side_effect = FileNotFoundError()
    result = runner.invoke(nutrition_cli, ["-v", "docker", "start"])
    _helper(result, dockerobj, dockerpty, open_env)
