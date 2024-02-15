from .apps import APPS, NUTRITION
from .docker import DEV_IMGS

from . import DEV

CHART = "chart"
IMAGE = "image"
ALL = "all"
DEV_IMG = "{}-image".format(DEV)
ACTIONS = [CHART, IMAGE]

TEMPLATE = "{}.{}"
DEV_TEMPLATE = "{}{}.{}"
TASKS_STRS = [TEMPLATE.format(NUTRITION, CHART)]

TASKS = {
    NUTRITION: {
        CHART: False,
    }
}


for app in APPS:
    for action in ACTIONS + [ALL]:
        TASKS_STRS.append(TEMPLATE.format(app, action))

    TASKS[app] = {}
    for action in ACTIONS:
        TASKS[app][action] = False

    if app in DEV_IMGS:
        TASKS[app][DEV_IMG] = False
