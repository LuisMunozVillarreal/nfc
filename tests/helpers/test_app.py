import itertools

from ntc.helpers.app import App, Nutrition


def _app_helper(mock, expected_data):
    app = App("any_app", "some_directory")
    app.increase_version()
    mock.return_value.write.assert_called_once_with(expected_data)


def _chart_helper(mock, expected_data):
    app = App("any_app", "some_directory")
    app.increase_chart_version()
    mock.return_value.write.assert_called_once_with(expected_data)


def test_increase_app_version_from_prod(git, time, open_prod_app_chart):
    expected_data = """appVersion: 0.1.70-dev-1-adfab93-1614735144
version: 0.1.68
"""
    _app_helper(open_prod_app_chart, expected_data)


def test_increase_app_version_from_dev(git, time, open_dev_app_chart):
    expected_data = """appVersion: 0.1.70-dev-2-adfab93-1614735144
version: 0.1.68-dev-2
"""
    _app_helper(open_dev_app_chart, expected_data)


def test_increase_chart_version_from_prod(git, time, open_prod_app_chart):
    expected_data = """appVersion: 0.1.70
version: 0.1.68-dev-1
"""
    _chart_helper(open_prod_app_chart, expected_data)


def test_increase_chart_version_from_dev(git, time, open_dev_app_chart):
    expected_data = """appVersion: 0.1.70-dev-1-adfab93-1614735144
version: 0.1.68-dev-3
"""
    _chart_helper(open_dev_app_chart, expected_data)
