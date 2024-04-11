from typing import Any

from exceptions import TokenizationError
from models import TokenType, Token


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0

    def get_next_token(self) -> Token:
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            
            if self.text[self.pos:self.pos+2] == '..':
                self.skip_comment()
                continue

            if self.pos >= len(self.text):
                return Token(TokenType.EOF, None)

            current_char = self.text[self.pos]

            if current_char == "'":
                return self.tokenize_string()
            
            elif current_char == '+':
                self.pos += 1
                return Token(TokenType.PLUS, '+')
            
            elif current_char == '-':
                self.pos += 1
                return Token(TokenType.MINUS, '-')
            
            elif current_char == '*':
                self.pos += 1
                return Token(TokenType.MULTIPLY, '*')
            
            elif current_char == '/':
                self.pos += 1
                return Token(TokenType.DIVIDE, '/')
            
            elif current_char == '=':
                self.pos += 1
                return Token(TokenType.ASSIGN, '=')
            
            elif current_char.isdigit():
                return self.tokenize_number()

            elif current_char.isalpha() or current_char == '_':
                return self.tokenize_identifier()

            else:
                raise TokenizationError(f"Unrecognized character '{current_char}'", self.pos)

        return Token(TokenType.EOF, None)

    def skip_comment(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self.pos += 1
        # Move past the newline character as well
        self.pos += 1 if self.pos < len(self.text) and self.text[self.pos] == '\n' else 0

    def tokenize_number(self) -> Token:
        """Tokenize a sequence of digits (an integer number)."""
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        num_str = self.text[start_pos:self.pos]
        return Token(TokenType.NUMBER, num_str)
    
    def tokenize_identifier(self) -> Token:
        """Tokenize an identifier, which can contain alphabetic characters and underscores."""
        start_pos = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        ident_str = self.text[start_pos:self.pos]

        token_type = TokenType.IDENTIFIER
        if ident_str == 'p':
            token_type = TokenType.PRINT

        return Token(token_type, ident_str)
    
    def tokenize_string(self) -> Token:
        self.pos += 1  # Skip the opening quote
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != "'":
            self.pos += 1

        if self.pos >= len(self.text):
            raise TokenizationError("Unterminated string literal", start_pos)
        
        string_value = self.text[start_pos:self.pos]
        self.pos += 1  # Skip the closing quote
        return Token(TokenType.STRING, string_value)