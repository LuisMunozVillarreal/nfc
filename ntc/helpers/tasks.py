import copy

from ..cfg.apps import NUTRITION
from ..cfg.environments import DEV_ENV, STAGING_ENV
from ..cfg.tasks import ACTIONS, ALL, CHART, DEV_IMG, IMAGE, TASKS


def computed_tasks(tasks, env=STAGING_ENV):
    computed_tasks = copy.deepcopy(TASKS)

    for task in tasks:
        app, action = task.split(".")
        if env == DEV_ENV:
            if action == IMAGE:
                computed_tasks[app][DEV_IMG] = True
            continue

        if action == ALL:
            for act in ACTIONS:
                computed_tasks[app][act] = True
            computed_tasks[NUTRITION][CHART] = True
        else:
            computed_tasks[app][action] = True

        if action == CHART:
            computed_tasks[NUTRITION][CHART] = True

    return computed_tasks
