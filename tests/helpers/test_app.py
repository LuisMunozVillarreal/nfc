import itertools

from ntc.cfg.environments import PROD_ENV, STAGING_ENV
from ntc.helpers.app import App, Nutrition


def _app_helper(mock, expected_data, env=STAGING_ENV, fix=False):
    app = App("any_app", "some_directory", env)
    app.increase_version(fix)
    mock.return_value.write.assert_called_once_with(expected_data)


def test_increase_app_version_from_prod_version_for_staging(
    git, time, open_prod_app_chart
):
    expected_data = (
        "appVersion: 0.1.70+dev-adfab93-1614735144\n"  #
        "version: 0.1.68\n"
    )
    _app_helper(open_prod_app_chart, expected_data)


def test_increase_app_version_from_prod_version_for_prod(
    git, time, open_prod_app_chart
):
    expected_data = (
        "appVersion: 0.2.0\n"  #
        "version: 0.1.68\n"
    )
    _app_helper(open_prod_app_chart, expected_data, PROD_ENV)


def test_increase_app_version_from_prod_version_for_prod_fix(
    git, time, open_prod_app_chart
):
    expected_data = (
        "appVersion: 0.1.71\n"  #
        "version: 0.1.68\n"
    )
    _app_helper(open_prod_app_chart, expected_data, PROD_ENV, True)


def test_increase_app_version_from_staging_version_for_staging(
    git, time, open_staging_app_chart
):
    expected_data = (
        "appVersion: 0.1.70+dev-adfab93-1614735144\n"
        "version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _app_helper(open_staging_app_chart, expected_data)


def test_increase_app_version_from_staging_version_for_prod(
    git, time, open_staging_app_chart
):
    expected_data = (
        "appVersion: 0.2.0\n"
        "version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _app_helper(open_staging_app_chart, expected_data, PROD_ENV)


def test_increase_app_version_from_staging_version_for_prod_fix(
    git, time, open_staging_app_chart
):
    expected_data = (
        "appVersion: 0.1.71\n"
        "version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _app_helper(open_staging_app_chart, expected_data, PROD_ENV, True)


def test_increase_webapp_version(git, time, open_staging_app_chart, open_package_json):
    expected_data = """{\n  "version": "0.2.0"\n}"""
    app = App("webapp", "some_directory", PROD_ENV)
    app.increase_version()
    assert open_package_json.return_value.write.call_args_list[0][0][0] == expected_data


def _chart_helper(mock, expected_data, env=STAGING_ENV):
    app = App("any_app", "some_directory", env)
    app.increase_chart_version()
    mock.return_value.write.assert_called_once_with(expected_data)


def test_increase_chart_version_from_prod_version_for_staging(
    git, time, open_prod_app_chart
):
    expected_data = (
        "appVersion: 0.1.70\n"  #
        "version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _chart_helper(open_prod_app_chart, expected_data)


def test_increase_chart_version_from_prod_version_for_prod(
    git, time, open_prod_app_chart
):
    expected_data = (
        "appVersion: 0.1.70\n"  #
        "version: 0.2.0\n"
    )
    _chart_helper(open_prod_app_chart, expected_data, env=PROD_ENV)


def test_increase_chart_version_from_staging_version_for_staging(
    git, time, open_staging_app_chart
):
    expected_data = (
        "appVersion: 0.1.70+dev-adfab93-1614735144\n"
        "version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _chart_helper(open_staging_app_chart, expected_data)


def test_increase_chart_version_from_staging_version_for_prod(
    git, time, open_staging_app_chart
):
    expected_data = (
        "appVersion: 0.1.70+dev-adfab93-1614735144\n"
        "version: 0.2.0\n"
    )
    _chart_helper(open_staging_app_chart, expected_data, env=PROD_ENV)


def _deps_helper(mock, expected_data):
    new_iter = itertools.tee(mock.side_effect)
    mock.side_effect = new_iter[1]
    inner_mock = list(new_iter[0])[0]

    nutrition = Nutrition("some_directory")
    app = App("backend", "some_directory")
    app.increase_version()
    nutrition.add_app(app)
    nutrition.update_release_versions()

    inner_mock.write.assert_called_once_with(expected_data)


def test_update_dep_versions_from_prod_version(git, time, open_prod_helmfile):
    expected_data = (
        "releases:\n"  #
        "- name: backend\n"  #
        "  version: 0.1.68\n"
    )
    _deps_helper(open_prod_helmfile, expected_data)


def test_update_dep_versions_from_staging_version(
    git, time, open_staging_helmfile
):
    expected_data = (
        "releases:\n"
        "- name: backend\n"
        "  version: 0.1.68+dev-adfab93-1614735144\n"
    )
    _deps_helper(open_staging_helmfile, expected_data)


def test_nutrition_prod_helmfile(open_prod_helmfile):
    # When
    Nutrition("some_dir", PROD_ENV)

    # Then
    assert "20-nutrition-production.yaml" in str(open_prod_helmfile.call_args)
