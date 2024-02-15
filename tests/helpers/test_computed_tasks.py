import copy

from ntc.cfg.environments import DEV_ENV
from ntc.helpers.tasks import computed_tasks

from .. import EXPECTED_TASKS


def test_computed_tasks_only_main():
    tasks_str = ["nutrition.chart"]

    tasks = copy.deepcopy(EXPECTED_TASKS)
    tasks["nutrition"]["chart"] = True

    assert tasks == computed_tasks(tasks_str)


def test_computed_tasks_action_all():
    tasks_str = ["webapp.all"]

    tasks = copy.deepcopy(EXPECTED_TASKS)
    tasks["nutrition"]["chart"] = True
    tasks["webapp"]["image"] = True
    tasks["webapp"]["chart"] = True

    assert tasks == computed_tasks(tasks_str)


def test_computed_tasks_only_dev_img():
    tasks_str = ["webapp.image", "reverse-proxy.all"]

    tasks = copy.deepcopy(EXPECTED_TASKS)
    tasks["webapp"]["dev-image"] = True

    assert tasks == computed_tasks(tasks_str, DEV_ENV)


def test_computed_tasks_only_combi():
    tasks_str = ["webapp.image", "reverse-proxy.all"]

    tasks = copy.deepcopy(EXPECTED_TASKS)
    tasks["webapp"]["image"] = True
    tasks["nutrition"]["chart"] = True
    tasks["reverse-proxy"]["image"] = True
    tasks["reverse-proxy"]["chart"] = True

    assert tasks == computed_tasks(tasks_str)
