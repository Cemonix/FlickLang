from tests.utils import run_flicklang_test


def test_arithmetic_operations() -> None:
    source_code = """
        a = 10 + 5
        b = 20 - 5
        c = 5 * 2
        d = 10 / 2
        e = 10 % 2
        p a
        p b
        p c
        p d
        p e
    """
    expected_output = "15\n15\n10\n5.0\n0\n"
    run_flicklang_test(source_code, expected_output)