import io
from contextlib import redirect_stdout

from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.interpreter import Interpreter


def run_flicklang_test(source_code: str, expected_output: str) -> None:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()

    f = io.StringIO()
    with redirect_stdout(f):
        interpreter.interpret(program)

    output = f.getvalue()
    assert (
        output == expected_output
    ), f"Expected output does not match actual output.\nExpected:\n{expected_output}\nGot:\n{output}"