"""Tests for ntc docker push command."""


from tests import assert_exit_code
from ntc import nutrition_cli


def test_docker_push(runner, dockerobj):
    """Test ntc docker push command."""
    dockerobj.return_value.images.push.return_value = [
        {"stream": "hola", "status": "hola"},
        "hola",
    ]
    result = runner.invoke(nutrition_cli, ["docker", "push"])
    assert_exit_code(result, 0)
    assert "Pushing" in result.output
    dockerobj.assert_called_once()
    dockerobj.return_value.images.push.assert_called_once()


def test_docker_push_error(runner, dockerobj):
    """Test ntc docker push command."""
    dockerobj.return_value.images.push.return_value = [
        {"errorDetail": "hola"},
    ]
    result = runner.invoke(nutrition_cli, ["docker", "push"])
    assert_exit_code(result, 1)
    assert "Pushing" in result.output
    assert "push failed" in result.exception.args[0]
    dockerobj.assert_called_once()
    dockerobj.return_value.images.push.assert_called_once()
