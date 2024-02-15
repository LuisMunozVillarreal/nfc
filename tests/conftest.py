"""Test config for Nutrition CLI."""


import pytest
from click.testing import CliRunner

CONTENT = """[DEFAULT]
WorkDir = /home/nutrition/repos/nutrition/
"""


@pytest.fixture(name="conf_file", autouse=True)
def conf_file(tmp_path):
    config_dir = tmp_path / "test"
    config_dir.mkdir()
    config_file = config_dir / ".ntcrc"
    config_file.write_text(CONTENT)
    return config_file


@pytest.fixture(name="git_rev_parse", autouse=True)
def _git_rev_parse(mocker, conf_file):
    mock = mocker.patch("ntc.helpers.config.git.Repo")
    mock.return_value.git.rev_parse.return_value = \
        str(conf_file.parent)
    return mock


@pytest.fixture(name="runner")
def _runner():
    """CliRunner."""
    return CliRunner()


@pytest.fixture(name="git")
def _git(mocker):
    """Git mock."""
    mock = mocker.patch("ntc.helpers.tag.git.Repo")
    mock.return_value.head.object.hexsha = "adfab930"


@pytest.fixture(name="time")
def _time(mocker):
    """Time mock."""
    mock = mocker.patch("ntc.helpers.tag.time.time")
    mock.return_value = "1614735144"


@pytest.fixture(name="dockerobj")
def _docker_mock(mocker, git):
    """Docker mock."""
    return mocker.patch("docker.from_env")


@pytest.fixture(name="dockerpty")
def _dockerpty(mocker):
    """Dockerpty mock."""
    return mocker.patch("ntc.cmds.docker.start.dockerpty.start")


@pytest.fixture(name="os_fsync")
def _os_fsync(mocker):
    return mocker.patch("ntc.helpers.chart.os.fsync")


@pytest.fixture(name="open_prod_app_chart")
def _open_prod_app_chart(mocker, os_fsync):
    """Open mock."""
    data = """
    appVersion: 0.1.70
    version: 0.1.68
    """
    return mocker.mock_open(
        mocker.patch("ntc.helpers.chart.open"), data)


@pytest.fixture(name="open_dev_app_chart")
def _open_dev_app_chart(mocker, os_fsync):
    """Open mock."""
    data = """
    appVersion: 0.1.70-dev-1-adfab93-1614735144
    version: 0.1.68-dev-2
    """
    return mocker.mock_open(
        mocker.patch("ntc.helpers.chart.open"), data)


@pytest.fixture(name="open_prod_main_chart")
def _open_prod_main_chart(mocker, open_prod_app_chart):
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


@pytest.fixture(name="open_dev_main_chart")
def _open_dev_main_chart(mocker, open_dev_app_chart):
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


@pytest.fixture(name="open_env")
def _open_env(mocker):
    """Open mock."""
    data = """
      HOLA=hola
      ADIOS=adios
    """
    return mocker.mock_open(
        mocker.patch("ntc.cmds.docker.start.open"), data)


@pytest.fixture(name="sh")
def _sh(mocker):
    """sh mock."""
    return mocker.patch("sh.Command")


@pytest.fixture(name="ntcconfig", autouse=True)
def _ntcconfig(mocker):
    config = {
        "DEFAULT": {
            "WorkDir": "."
        },
    }
    mock = mocker.patch("ntc.NtcConfig")
    mock.return_value = config
    return mock
