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
        if self.position is not None:
            return f"SyntaxError at position {self.position}: {self.message}"
        else:
            return f"SyntaxError: {self.message}"

class TokenizationError(FlickLangError):
    def __init__(self, message: str, position: int | None = None) -> None:
        super().__init__(message)
        self.position = position

    def __str__(self) -> str:
        if self.position is not None:
            return f"TokenizationError at position {self.position}: {self.message}"
        else:
            return f"TokenizationError: {self.message}"

class ExecutionError(FlickLangError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"ExecutionError: {self.message}"
