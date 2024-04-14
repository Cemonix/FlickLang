import pytest

from flicklang.exceptions import ExecutionError
from tests.utils import run_flicklang_test


def test_error_handling() -> None:
    source_code = """
        x = 10 / 0
        p x
    """
    with pytest.raises(ExecutionError) as exc_info:
        run_flicklang_test(source_code, "")
    assert "Division by zero" in str(exc_info.value)
