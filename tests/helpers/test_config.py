import pytest

from ntc.helpers.config import NtcConfig


def test_ntc_config(git_rev_parse):
    config = NtcConfig()
    assert config["DEFAULT"]["WorkDir"] == "/home/nutrition/repos/nutrition/"
