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


def _deps_helper(mock, expected_data):
    new_iter = itertools.tee(mock.side_effect)
    mock.side_effect = new_iter[1]
    inner_mock = list(new_iter[0])[0]

    nutrition = Nutrition("some_directory")
    app = App("reverse-proxy", "some_directory")
    app.increase_version()
    nutrition.add_app(app)
    nutrition.update_dep_versions()

    inner_mock.write.assert_called_once_with(expected_data)


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


def test_update_dep_versions_from_prod(git, time, open_prod_main_chart):
    expected_data = """dependencies:
- name: traefik
  version: 1.87.2
- name: reverse-proxy
  version: 0.1.68
version: 1.2.39
"""
    _deps_helper(open_prod_main_chart, expected_data)


def test_update_dep_versions_from_dev(git, time, open_dev_main_chart):
    expected_data = """dependencies:
- name: traefik
  version: 1.87.2
- name: reverse-proxy
  version: 0.1.68-dev-2
version: 1.2.39-dev-2
"""
    _deps_helper(open_dev_main_chart, expected_data)
