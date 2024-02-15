"""Tests for ntc kubectl command."""


from tests import assert_exit_code
from ntc import nutrition_cli


def test_kubectl_use_context(runner, sh):
    """Test kubectl use-context command."""
    result = runner.invoke(nutrition_cli, ["kubectl", "use-context"])
    assert_exit_code(result, 0)
    args = sh.return_value.call_args.args
    assert "staging" in args[2]


def test_kubectl_use_context_production(runner, sh):
    """Test kubectl use-context command for production."""
    result = runner.invoke(
        nutrition_cli, ["-e", "production", "kubectl", "use-context"])
    assert_exit_code(result, 0)
    args = sh.return_value.call_args.args
    assert "production" in args[2]
