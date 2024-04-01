import os

from ntc.cfg.helm import CHARTS_PATH, HELM_FILE_PRODUCTION, HELM_FILE_STAGING

from ntc.cfg import DEV
from ntc.cfg.apps import APPS, WEBAPP
from ntc.cfg.environments import STAGING_ENV, PROD_ENV

from .chart import Chart
from .json import Json
from .tag import generate_tag
from .yaml import Yaml


class App:
    def __init__(self, name, work_dir, env=STAGING_ENV):
        self._name = name
        self._work_dir = work_dir
        self._env = env

        chart_path = os.path.join(self._work_dir, name, CHARTS_PATH)
        self._chart = Chart(chart_path)

        if name == WEBAPP:
            package_path = os.path.join(self._work_dir, name)
            self._package = Json(package_path)

    @property
    def name(self):
        return self._name

    @property
    def app_version(self):
        return self._chart.app_version

    @property
    def chart_version(self):
        return self._chart.version

    @property
    def env(self):
        return self._env

    def _next_version(self, version, fix=False):
        index = 2 if fix else 1
        version = version.split("+")[0]
        version = version.split(".")
        if not fix:
            version[2] = "0"
        version[index] = str(int(version[index]) + 1)
        return ".".join(version)

    def _next_app_version(self, fix):
        self._chart.app_version = self._next_version(
            self._chart.app_version, fix
        )

    def _next_chart_version(self):
        self._chart.version = self._next_version(self._chart.version)

    def increase_version(self, fix=False):
        if self.env == STAGING_ENV:
            tag = generate_tag(self._work_dir, self._name)
            semver = self.app_version.split("+")[0]
            self._chart.app_version = "{}+dev-{}".format(semver, tag)
        else:
            self._next_app_version(fix)

        if self._name == WEBAPP:
            self._package._json_content["version"] = self._chart.app_version
            self._package.save()

        self._chart.save()

    def increase_chart_version(self):
        if self.env == STAGING_ENV:
            tag = generate_tag(self._work_dir, self._name)
            semver = self._chart.version.split("+")[0]
            self._chart.version = "{}+dev-{}".format(semver, tag)
        else:
            self._next_chart_version()

        self._chart.save()


class Nutrition(Yaml):
    def __init__(self, work_dir, env=STAGING_ENV):
        helmfile = HELM_FILE_STAGING
        if env == PROD_ENV:
            helmfile = HELM_FILE_PRODUCTION
        super().__init__(helmfile)
        self._env = env
        self._apps = {}

    def add_app(self, app):
        self._apps[app.name] = app

    def update_release_versions(self):
        """

        Release in the context of helmfile.
        """
        for app in self._apps:
            self._yaml_content["releases"][APPS.index(app)]["version"] = (
                self._apps[app].chart_version
            )

        self.save()
