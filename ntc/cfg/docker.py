"""Nutrition CLI docker config."""

from .apps import BACKEND, WEBAPP

REGISTRY = ""

DOCKER_DIR = "platform/docker"
DOCKERFILE = "Dockerfile"

DEV_IMGS = [BACKEND, WEBAPP]
LATEST = "latest"

ASH = "/bin/ash"
BASH = "/bin/bash"
