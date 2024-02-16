import traceback


EXPECTED_TASKS = {
    "backend": {
        "chart": False,
        "image": False,
    },
    "webapp": {
        "chart": False,
        "image": False,
    },
}


def assert_exit_code(result, expected_code):
    assert result.exit_code == expected_code, traceback.print_exception(
        *result.exc_info
    )
