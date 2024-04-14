from typing import Any

from flicklang.models import EOFToken, Token
        

class FlickLangError(Exception):
    """Base class for errors in FlickLang."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class SyntaxError(FlickLangError):
    def __init__(self, message: str, position: int | None = None) -> None:
        super().__init__(message)
        self.position = position

    def __str__(self) -> str:
        position_info = f"at position {self.position}" if self.position is not None else ""
        return f"SyntaxError{ position_info}: {self.message}"


class TokenizationError(FlickLangError):
    def __init__(self, message: str, position: int | None = None) -> None:
        super().__init__(message)
        self.position = position

    def __str__(self) -> str:
        position_info = f"at position {self.position}" if self.position is not None else ""
        return f"TokenizationError {position_info}: {self.message}"


class ParsingError(FlickLangError):
    """Exception raised for errors in the parsing process."""
    def __init__(self, message: str, token: Token | EOFToken) -> None:
        super().__init__(f"{message} {token}")
        self.message = message
        self.token = token

    def __str__(self) -> str:
        return f"ParsingError: {self.message} at token {self.token}"

class ExecutionError(FlickLangError):
    def __str__(self) -> str:
        return f"ExecutionError: {self.message}"


class ReturnSignal(FlickLangError):
    """Exception used to signal a return from a function with a value."""
    def __init__(self, value: Any) -> None:
        super().__init__(str(value))
        self.value = value