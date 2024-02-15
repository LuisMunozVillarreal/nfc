import sys

import click
import sh


class Command():
    def __init__(self, cmd, debug):
        self.__cmd = sh.Command(cmd)
        self.__name = cmd
        self.__debug = debug

    def run(self, args, kwargs={}):
        if self.__debug:
            kwargs_str = ""
            if kwargs:
                kwargs_str = " ".join(kwargs.values())
            msg = "debug: executed cmd: {} {} {}".format(
                self.__name, " ".join(args), kwargs_str)
            click.echo(msg)

        self.__cmd(*args, _out=sys.stdout, _err=sys.stderr, **kwargs)
