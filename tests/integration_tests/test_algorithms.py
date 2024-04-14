import pytest

from flicklang.exceptions import ExecutionError
from tests.utils import run_flicklang_test


def test_factorial_calculation() -> None:
    source_code = """
        n = 5
        fact = 1
        w n gr 0 {
            fact = fact * n
            n = n - 1
        }
        p fact
    """
    expected_output = "120\n"
    run_flicklang_test(source_code, expected_output)


def test_bubble_sort() -> None:
    source_code = """
        array = [5, 3, 7, 10]
        array_len = 4
        .. Bubble sort
        i = 0
        w i ls array_len
        {
            j = 0
            w j ls array_len
            {
                if array[i] ls array[j]
                {
                    temp = array[i]
                    array[i] = array[j]
                    array[j] = temp
                }
                j = j + 1
            }
            i = i + 1 
        }

        i = 0
        w i ls array_len
        {
            p array[i]
            i = i + 1
        }
    """
    expected_output = "3\n5\n7\n10\n"
    run_flicklang_test(source_code, expected_output)
