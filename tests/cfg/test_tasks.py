from ntc.cfg.tasks import TASKS, TASKS_STRS

from .. import EXPECTED_TASKS


def test_available_tasks():
    expected_tasks = [
        "nutrition.chart",
        "api.chart",
        "api.image",
        "api.all",
        "reverse-proxy.chart",
        "reverse-proxy.image",
        "reverse-proxy.all",
        "webapp.chart",
        "webapp.image",
        "webapp.all",
    ]
    assert expected_tasks == TASKS_STRS


def test_task():
    assert EXPECTED_TASKS == TASKS
