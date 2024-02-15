import json
import os


PACKAGE_JSON = "package.json"


class Json:
    def __init__(self, json_path):
        self.__json_file = open(os.path.join(json_path, PACKAGE_JSON), "r+")
        self.__json_content = json.load(self.__json_file)

    def __del__(self):
        self.save()
        self.__json_file.close()

    def save(self):
        self.__json_file.seek(0)
        self.__json_file.truncate()
        self.__json_file.write(json.dumps(self.__json_content, indent=2))
        self.__json_file.write("\n")
        self.__json_file.flush()
        os.fsync(self.__json_file.fileno())

    @property
    def version(self):
        return self.__json_content["version"]

    @version.setter
    def version(self, version):
        self.__json_content["version"] = version
