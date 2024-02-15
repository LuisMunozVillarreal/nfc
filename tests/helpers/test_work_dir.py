import pytest

from ntc.helpers.workdir import get_work_dir


def test_ntc_work_dir(git_rev_parse):
    assert get_work_dir() == "/home/nutrition/repos/nutrition/"
