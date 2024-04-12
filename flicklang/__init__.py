from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.interpreter import Interpreter

# TODO: Get program as argument
# Example FlickLang program
source_code = """
a = 10 b = 5
p a
p b
if a eq b
{
    p 'a is equal to b'
}
eli a gr b
{
    p 'a is greater then b'
}
el
{
    p 'a is not equal to b'
}
"""


def run_flicklang_program(source_code: str) -> None:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(program)


if __name__ == "__main__":
    run_flicklang_program(source_code)
