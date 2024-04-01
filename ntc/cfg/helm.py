"""Nutrition CLI helm config."""

from .apps import BACKEND

CHARTS_PATH = "platform/kube"
CHART_FILE = "Chart.yaml"

HELM_FILE_PATH = f"{CHARTS_PATH}/helmfile.d"
HELM_FILE_STAGING = f"{HELM_FILE_PATH}/10-nutrition-staging.yaml"
HELM_FILE_PRODUCTION = f"{HELM_FILE_PATH}/20-nutrition-production.yaml"
