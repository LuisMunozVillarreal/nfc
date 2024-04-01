import os

import yaml


class Yaml:
    def __init__(self, yaml_path):
        self._yaml_file = open(yaml_path, "r+")
        self._yaml_content = yaml.safe_load(self._yaml_file)

    def __del__(self):
        self.save()
        self._yaml_file.close()

    def save(self):
        self._yaml_file.seek(0)
        self._yaml_file.truncate()
        # import ipdb
        # ipdb.set_trace()
        self._yaml_file.write(yaml.dump(self._yaml_content))
        self._yaml_file.flush()
        # print(self._yaml_file.fileno())
        # print(os.fsync)
        os.fsync(self._yaml_file.fileno())
