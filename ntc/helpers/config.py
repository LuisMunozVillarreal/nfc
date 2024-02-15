import os

from configobj import ConfigObj
import git

from ntc.cfg import CONFIG_FILE


class NtcConfig():
    def __init__(self):
        self.__conf = ConfigObj(self.__config_file)

    @property
    def __config_file(self):
        git_repo = git.Repo(".", search_parent_directories=True)
        git_repo = git_repo.git.rev_parse("--show-toplevel")
        return os.path.join(git_repo, CONFIG_FILE)


    def __getitem__(self, attr):
        return self.__conf[attr]
