"""Nutrition CLI helm config."""


from .apps import API

CHARTS_PATH = "platform/kube"
CHART_FILE = "Chart.yaml"

MAIN_CHART = "nutrition"

PRODUCTION_VALUES_FILE = "production.values.yaml"

CHART_WITH_DEPS = [API]

POSTGRESQL_PASSWORD_CONF_VAR = "PostgresqlPassword"
