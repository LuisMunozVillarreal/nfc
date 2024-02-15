"""Nutrition CLI helm config."""


from .apps import BACKEND

CHARTS_PATH = "platform/kube"
CHART_FILE = "Chart.yaml"

MAIN_CHART = "nutrition"

PRODUCTION_VALUES_FILE = "production.values.yaml"
