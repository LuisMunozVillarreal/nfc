import traceback


EXPECTED_TASKS = {
    "api": {
        "chart": False,
        "image": False,
        "dev-image": False,
    },
    "nutrition": {
        "chart": False,
    },
    "webapp": {
        "chart": False,
        "image": False,
        "dev-image": False,
    },
    "reverse-proxy": {
        "chart": False,
        "image": False,
    },
}


def assert_exit_code(result, expected_code):
    assert result.exit_code == expected_code, traceback.print_exception(
        *result.exc_info)
