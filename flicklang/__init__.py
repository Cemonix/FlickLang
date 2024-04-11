from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.interpreter import Interpreter

# TODO: Get program as argument
# Example FlickLang program
source_code = """
p 5 + 2 * 3
x = 10
a=10 b=10 c=10
b = 5.5
p b
.. d = c 
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
