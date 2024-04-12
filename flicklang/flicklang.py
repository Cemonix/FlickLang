import argparse

from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.interpreter import Interpreter

flicklang_ascii = """
 ______ _ _      _    _                       
|  ____| (_)    | |  | |                      
| |__  | |_  ___| | _| |     __ _ _ __   __ _ 
|  __| | | |/ __| |/ / |    / _` | '_ \\ / _` |
| |    | | | (__|   <| |___| (_| | | | | (_| |
|_|    |_|_|\\___|_|\\_\\______\\__,_|_| |_|\\__, |
                                         __/ |
                                        |___/ 
            
FlickLang Interactive Mode. Type 'exit' to exit.
"""

def run_flicklang_program(source_code: str) -> None:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(program)

def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Run FlickLang programs.")
    arg_parser.add_argument("file_path", nargs='?', default=None, help="The FlickLang file to run")

    args = arg_parser.parse_args()

    if args.file_path:
        file_path = args.file_path
        print(f"Running FlickLang interpreter on file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
                run_flicklang_program(source_code)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        # Interactive mode
        print(flicklang_ascii)
        while True:
            try:
                source_code = input(">>> ")
                if source_code.strip().lower() == 'exit':
                    print("Exiting FlickLang Interactive Mode.")
                    break
                run_flicklang_program(source_code)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
