"""Application error definitions and handlers."""


class ApplicationError(Exception):
    """Custom application error with message and HTTP status code."""

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)
