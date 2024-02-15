"""Tests for ntc docker build command."""


import re

from tests import assert_exit_code
from ntc import nutrition_cli


def _helper(runner, dockerobj, cmd, build_output,
            exit_code, tag_regex, get_calls, app, build_args=None):
    # pylint: disable=too-many-arguments
    """Test helper."""
    dockerobj.return_value.api.build.return_value = build_output

    result = runner.invoke(nutrition_cli, cmd)
    assert_exit_code(result, exit_code)
    assert "Building" in result.output
    dockerobj.assert_called_once()
    dockerobj.return_value.api.build.assert_called_once()
    assert dockerobj.return_value.images.get.call_count == get_calls

    build_kwargs = dockerobj.return_value.api.build.call_args.kwargs
    assert re.match(tag_regex, build_kwargs["tag"])
    assert app in build_kwargs["path"]
    assert build_args == build_kwargs["buildargs"]


def test_docker_build(runner, dockerobj):
    """Test ntc docker build command."""
    _helper(
        runner, dockerobj,
        cmd=["docker", "build"],
        build_output=[{"stream": "hola"}, "hola"],
        exit_code=0,
        tag_regex=r"webapp:[a-f0-9]*-[0-9]*",
        get_calls=1,
        app="webapp",
        build_args={"ENV": "staging"},
    )


def test_docker_build_reverse_proxy(runner, dockerobj):
    """Test ntc docker build command."""
    _helper(
        runner, dockerobj,
        cmd=["docker", "--app", "reverse-proxy", "build"],
        build_output=[{"stream": "hola"}, "hola"],
        exit_code=0,
        tag_regex=r"reverse-proxy:[a-f0-9]*-[0-9]*",
        get_calls=1,
        app="reverse-proxy",
        build_args={"ENV": "staging"},
    )


def test_docker_build_dev_webapp(runner, dockerobj):
    """Test ntc docker build command."""
    _helper(
        runner, dockerobj,
        cmd=["-e", "dev", "docker", "build"],
        build_output=[{"stream": "hola"}, "hola"],
        exit_code=0,
        tag_regex=r"webapp-dev:[a-f0-9]*",
        get_calls=1,
        app="webapp",
    )


def test_docker_build_with_dockerfile(runner, dockerobj):
    """Test ntc docker build command."""
    _helper(
        runner, dockerobj,
        cmd=["docker", "build", "--dockerfile", "hola"],
        build_output=[{"stream": "hola"}, "hola"],
        exit_code=0,
        tag_regex=r"webapp:[a-f0-9]*-[0-9]*",
        get_calls=1,
        app="webapp",
        build_args={"ENV": "staging"},
    )


def test_docker_build_error(runner, dockerobj):
    """Test ntc docker build command when there is an error."""
    _helper(
        runner, dockerobj,
        cmd=["docker", "build"],
        build_output=[{"errorDetail": "hola"}],
        exit_code=1,
        tag_regex=r"webapp:[a-f0-9]*-[0-9]*",
        get_calls=0,
        app="webapp",
        build_args={"ENV": "staging"},
    )


def test_docker_build_production(runner, dockerobj):
    """Test ntc docker build command when env isn't staging."""
    _helper(
        runner, dockerobj,
        cmd=["--env", "production", "docker", "build"],
        build_output=[],
        exit_code=0,
        tag_regex=r"webapp:[a-f0-9]*",
        get_calls=1,
        app="webapp",
        build_args={"ENV": "production"},
    )
