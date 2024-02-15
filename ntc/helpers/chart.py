"""ntc helper module for Chart files."""


import os

from ntc.cfg.helm import CHART_FILE
import yaml


class Chart():
    def __init__(self, chart_path):
        self.__chart_file = open(os.path.join(chart_path, CHART_FILE), "r+")
        self.__chart_content = yaml.safe_load(self.__chart_file)

    def __del__(self):
        self.save()
        self.__chart_file.close()

    def save(self):
        self.__chart_file.seek(0)
        self.__chart_file.truncate()
        self.__chart_file.write(yaml.dump(self.__chart_content))
        self.__chart_file.flush()
        os.fsync(self.__chart_file.fileno())

    @property
    def version(self):
        return self.__chart_content["version"]

    @version.setter
    def version(self, version):
        self.__chart_content["version"] = version

    @property
    def app_version(self):
        return self.__chart_content["appVersion"]

    @app_version.setter
    def app_version(self, app_version):
        self.__chart_content["appVersion"] = app_version

    @property
    def dep_versions(self):
        return self.__chart_content["dependencies"]

    @dep_versions.setter
    def dep_versions(self, dep_versions):
        for dependency in self.__chart_content["dependencies"]:
            if dependency["name"] in dep_versions:
                dependency["version"] = dep_versions[dependency["name"]]
        self.save()
