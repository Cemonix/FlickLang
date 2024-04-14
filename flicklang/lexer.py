from lib2to3.pygram import Symbols
from typing import List

from flicklang.exceptions import TokenizationError
from flicklang.models import (
    Comparison,
    Keyword,
    SyntaxTokenType,
    Token,
    EOFToken,
    Operator,
    Symbol,
    Fundamental,
)


class Lexer:
    operators = set(op.value for op in Operator)
    symbols = set(sym.value for sym in Symbol)
    keywords_set = {item.value: item for item in Keyword}
    comparisons_set = {item.value: item for item in Comparison}

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.pos += 1
                continue

            if (
                self.pos + 1 < len(self.text)
                and self.text[self.pos : self.pos + 2] == ".."
            ):
                self.skip_comment()
                continue

            if self.pos >= len(self.text):
                break
            
            token = self.get_next_token()
            tokens.append(token)
            
        tokens.append(EOFToken(Fundamental.EOF))
        return tokens
        
    def get_next_token(self) -> Token | EOFToken:
        current_char = self.text[self.pos]
        if current_char in Lexer.operators:
            self.pos += 1
            return Token(Operator(current_char), current_char)
        elif current_char in Lexer.symbols:
            self.pos += 1
            return Token(Symbol(current_char), current_char)
        elif current_char == "'":
            return self.tokenize_string()
        elif current_char.isdigit():
            return self.tokenize_number()
        elif current_char.isalpha() or current_char == "_":
            return self.tokenize_syntax()
        else:
            raise TokenizationError(f"Unrecognized character '{current_char}'", self.pos)
   
    def skip_comment(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] != "\n":
            self.pos += 1
        # Move past the newline character as well
        self.pos += (
            1 if self.pos < len(self.text) and self.text[self.pos] == "\n" else 0
        )

    def tokenize_number(self) -> Token:
        """Tokenize a sequence of digits (an integer number)."""
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1

        # Check for a decimal point
        if self.pos < len(self.text) and self.text[self.pos] == ".":
            self.pos += 1  # Consume the dot
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

        num_str = self.text[start_pos : self.pos]
        return Token(Fundamental.NUMBER, num_str)

    def tokenize_string(self) -> Token:
        self.pos += 1  # Skip the opening quote
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != "'":
            self.pos += 1

        if self.pos >= len(self.text):
            raise TokenizationError("Unterminated string literal", start_pos)

        string_value = self.text[start_pos : self.pos]
        self.pos += 1  # Skip the closing quote
        return Token(Fundamental.STRING, string_value)
    
    def tokenize_syntax(self) -> Token:
        start_pos = self.pos
        while self.pos < len(self.text) and (
            self.text[self.pos].isalnum() or self.text[self.pos] == "_"
        ):
            self.pos += 1

        ident_str = self.text[start_pos : self.pos]
        token_type = self.determine_token_type(ident_str)
        return Token(token_type, ident_str)
    
    def determine_token_type(self, ident_str: str) -> SyntaxTokenType:
        if ident_str in Lexer.keywords_set:
            return Keyword[ident_str.upper()]
        
        if ident_str in Lexer.comparisons_set:
            return Comparison[ident_str.upper()]

        return Fundamental.IDENTIFIER
