"""Nutrition CLI docker config."""


from .apps import API, WEBAPP

REGISTRY = "eu.gcr.io/nutrition"

DOCKER_DIR = "platform/docker"
DOCKERFILE = "Dockerfile"
DOCKERFILE_DEV = "Dockerfile.dev"

DEV_IMGS = [API, WEBAPP]
LATEST = "latest"

ASH = "/bin/ash"
BASH = "/bin/bash"
ENV_FILE = ".env.development"

POSTGRES_DATA_DIR = "/var/lib/postgresql/11/main/"
