from ntc import nutrition_cli
from tests import assert_exit_code


def test_apply(runner, dockerobj, sh, open_staging_helmfile):
    # When
    result = runner.invoke(nutrition_cli, ["--debug", "cloud", "apply"])

    # Then
    assert_exit_code(result, 0)

    dockerobj.assert_called_once()
    dockerobj.return_value.api.build.assert_called_once()
    dockerobj.return_value.images.get.return_value.tag.assert_called()
    dockerobj.return_value.images.push.assert_called_once()

    sh.assert_called_once_with("helmfile")
    assert sh.return_value.call_args[0][0] == "apply"
