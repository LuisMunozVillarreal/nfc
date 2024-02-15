import os

from ntc.cfg.helm import CHARTS_PATH

from ntc.cfg import DEV
from ntc.cfg.apps import WEBAPP
from ntc.cfg.environments import STAGING_ENV, PROD_ENV

from .chart import Chart
from .json import Json
from .tag import generate_tag


class App():
    def __init__(self, name, work_dir, env=STAGING_ENV, chart_path=None):
        self.__name = name
        self.__work_dir = work_dir
        self.__env = env

        if not chart_path:
            chart_path = os.path.join(self.__work_dir, name, CHARTS_PATH)

        self._chart = Chart(chart_path)

        if name == WEBAPP:
            package_path = os.path.join(self.__work_dir, name)
            self._package = Json(package_path)

    @property
    def name(self):
        return self.__name

    @property
    def app_version(self):
        return self._chart.app_version

    @property
    def chart_version(self):
        return self._chart.version

    @property
    def env(self):
        return self.__env

    def __next_dev_build(self, version):
        dev_build = 1
        if DEV in version:
            dev_build = int(version.split("-")[2]) + 1
        return str(dev_build)

    def __next_version(self, version, fix=False):
        index = 2 if fix else 1
        version = version.split(".")
        if not fix:
            version[2] = "0"
        version[index] = str(int(version[index]) + 1)
        return ".".join(version)

    def __next_app_version(self, fix):
        self._chart.app_version = self.__next_version(
            self._chart.app_version, fix)

    def __next_chart_version(self):
        self._chart.version = self.__next_version(self._chart.version)

    def increase_version(self, dev=True, fix=False):
        if self.env == PROD_ENV:
            return

        if dev:
            tag = generate_tag(self.__work_dir, self.__name)
            dev_build = self.__next_dev_build(self.app_version)
            stable_part = self.app_version.split("-")[0]
            self._chart.app_version = "{}-dev-{}-{}".format(
                stable_part, dev_build, tag)
        else:
            self.__next_app_version(fix)

        if self.__name == WEBAPP:
            self._package.version = self._chart.app_version
            self._package.save()

        self._chart.save()

    def increase_chart_version(self, dev=True):
        if self.env == PROD_ENV:
            return

        if dev:
            dev_build = self.__next_dev_build(self._chart.version)
            stable_part = self._chart.version.split("-")[0]
            self._chart.version = "{}-dev-{}".format(stable_part, dev_build)
        else:
            self.__next_chart_version()

        self._chart.save()


class Nutrition(App):
    def __init__(self, work_dir, env=STAGING_ENV):
        super().__init__("nutrition", work_dir, env,
                         os.path.join(work_dir, CHARTS_PATH))
        self.__apps = {}

    @property
    def app_version(self):
        raise NotImplementedError(
            "Nutrition main chart doesn't have appVersion")

    def add_app(self, app):
        self.__apps[app.name] = app

    def update_dep_versions(self):
        if self.env == PROD_ENV:
            return

        dep_versions = {}
        for app in self.__apps:
            dep_versions[app] = self.__apps[app].chart_version
        self._chart.dep_versions = dep_versions
