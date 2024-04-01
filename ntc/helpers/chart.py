"""ntc helper module for Chart files."""

import os

from ntc.cfg.helm import CHART_FILE

from .yaml import Yaml


class Chart(Yaml):
    def __init__(self, chart_path):
        super().__init__(os.path.join(chart_path, CHART_FILE))

    @property
    def version(self):
        return self._yaml_content["version"]

    @version.setter
    def version(self, version):
        self._yaml_content["version"] = version

    @property
    def app_version(self):
        return self._yaml_content["appVersion"]

    @app_version.setter
    def app_version(self, app_version):
        self._yaml_content["appVersion"] = app_version
        