"""Tests for ntc docker tag command."""

from tests import assert_exit_code
from ntc import nutrition_cli


def test_docker_tag(runner, dockerobj):
    """Test ntc docker start command."""
    result = runner.invoke(nutrition_cli, ["docker", "tag"])
    assert_exit_code(result, 0)
    assert "Tagging" in result.output
    dockerobj.assert_called_once()
    mock = dockerobj.return_value.images.get
    mock.assert_called_once()
    mock.return_value.tag.assert_called_once()


def test_docker_tag_error(runner, dockerobj):
    """Test ntc docker start command when there is an error."""
    mock = dockerobj.return_value.images.get
    mock.return_value.tag.return_value = False
    result = runner.invoke(nutrition_cli, ["docker", "tag"])
    assert_exit_code(result, 0)
    assert "Tagging" in result.output
    dockerobj.assert_called_once()
    mock.assert_called_once()
    mock.return_value.tag.assert_called_once()
