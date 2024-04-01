"""Test config for Nutrition CLI."""

import pytest
from click.testing import CliRunner


@pytest.fixture(autouse=True)
def git_rev_parse(mocker):
    mock = mocker.patch("ntc.helpers.workdir.git.Repo")
    mock.return_value.git.rev_parse.return_value = (
        "/home/nutrition/repos/nutrition/"
    )
    return mock


@pytest.fixture
def runner():
    """CliRunner."""
    return CliRunner()


@pytest.fixture
def git(mocker):
    """Git mock."""
    mock = mocker.patch("ntc.helpers.tag.git.Repo")
    mock.return_value.head.object.hexsha = "adfab930"


@pytest.fixture
def time(mocker):
    """Time mock."""
    mock = mocker.patch("ntc.helpers.tag.time.time")
    mock.return_value = 1614735144


@pytest.fixture
def dockerobj(mocker, git):
    """Docker mock."""
    return mocker.patch("docker.from_env")


@pytest.fixture
def dockerpty(mocker):
    """Dockerpty mock."""
    return mocker.patch("ntc.cmds.docker.start.dockerpty.start")


@pytest.fixture
def os_fsync(mocker):
    return mocker.patch("ntc.helpers.yaml.os.fsync")


@pytest.fixture
def open_prod_app_chart(mocker, os_fsync):
    data = """
        appVersion: 0.1.70
        version: 0.1.68
    """
    return mocker.mock_open(mocker.patch("ntc.helpers.yaml.open"), data)


@pytest.fixture
def open_staging_app_chart(mocker, os_fsync):
    data = """
        appVersion: 0.1.70+dev-adfab93-1614735144
        version: 0.1.68+dev-adfab93-1614735144
    """
    return mocker.mock_open(mocker.patch("ntc.helpers.yaml.open"), data)


@pytest.fixture
def open_package_json(mocker, os_fsync):
    data = """{ "version": "0.1.68" }"""
    return mocker.mock_open(mocker.patch("ntc.helpers.json.open"), data)


@pytest.fixture
def open_prod_helmfile(mocker, open_prod_app_chart):
    data = """
        releases:
          - name: backend
            version: 0.1.68
    """
    handlers = [
        mocker.mock_open(read_data=data).return_value,
        open_prod_app_chart.return_value,
    ]
    open_prod_app_chart.side_effect = handlers
    return open_prod_app_chart


@pytest.fixture
def open_staging_helmfile(mocker, open_staging_app_chart):
    data = """
        releases:
          - name: backend
            version: 0.1.68+dev-adfab93-1614735144
    """
    handlers = [
        mocker.mock_open(read_data=data).return_value,
        open_staging_app_chart.return_value,
    ]
    open_staging_app_chart.side_effect = handlers
    return open_staging_app_chart


@pytest.fixture
def open_env(mocker):
    """Open mock."""
    data = """
        HOLA=hola
        ADIOS=adios
    """
    return mocker.mock_open(mocker.patch("ntc.cmds.docker.start.open"), data)


@pytest.fixture
def sh(mocker):
    """sh mock."""
    return mocker.patch("sh.Command")
