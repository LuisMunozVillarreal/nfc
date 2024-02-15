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
    mock.return_value = "1614735144"


@pytest.fixture
def docker_mock(mocker, git):
    """Docker mock."""
    return mocker.patch("docker.from_env")


@pytest.fixture
def dockerpty(mocker):
    """Dockerpty mock."""
    return mocker.patch("ntc.cmds.docker.start.dockerpty.start")


@pytest.fixture
def os_fsync(mocker):
    return mocker.patch("ntc.helpers.chart.os.fsync")


@pytest.fixture
def open_prod_app_chart(mocker, os_fsync):
    """Open mock."""
    data = """
    appVersion: 0.1.70
    version: 0.1.68
    """
    return mocker.mock_open(
        mocker.patch("ntc.helpers.chart.open"), data)


@pytest.fixture
def open_dev_app_chart(mocker, os_fsync):
    """Open mock."""
    data = """
    appVersion: 0.1.70-dev-1-adfab93-1614735144
    version: 0.1.68-dev-2
    """
    return mocker.mock_open(
        mocker.patch("ntc.helpers.chart.open"), data)


@pytest.fixture
def open_prod_main_chart(mocker, open_prod_app_chart):
    """Open mock."""
    data = """
    version: 1.2.39
    dependencies:
      - name: traefik
        version: 1.87.2
      - name: reverse-proxy
        version: 0.1.70
    """
    handlers = [
        mocker.mock_open(read_data=data).return_value,
        open_prod_app_chart.return_value,
    ]
    open_prod_app_chart.side_effect = handlers
    return open_prod_app_chart


@pytest.fixture
def open_dev_main_chart(mocker, open_dev_app_chart):
    """Open mock."""
    data = """
    version: 1.2.39-dev-2
    dependencies:
      - name: traefik
        version: 1.87.2
      - name: reverse-proxy
        version: 0.1.70-dev-3-adfab93-1614735144
    """
    handlers = [
        mocker.mock_open(read_data=data).return_value,
        open_dev_app_chart.return_value,
    ]
    open_dev_app_chart.side_effect = handlers
    return open_dev_app_chart


@pytest.fixture
def open_env(mocker):
    """Open mock."""
    data = """
      HOLA=hola
      ADIOS=adios
    """
    return mocker.mock_open(
        mocker.patch("ntc.cmds.docker.start.open"), data)


@pytest.fixture
def sh(mocker):
    """sh mock."""
    return mocker.patch("sh.Command")
