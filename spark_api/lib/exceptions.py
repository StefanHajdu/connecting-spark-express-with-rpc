"""Custom exceptions for the Spark API project."""


class DuplicateSessionException(Exception):
    """Raised when attempting to create a session that already exists."""

    def __init__(self, message='Duplicate sessions'):
        super().__init__(message)


class LoadNodeRemovalException(Exception):
    """Raised when attempting to remove a load node from the plan."""

    def __init__(self, message='Cannot remove load node from plan'):
        super().__init__(message)


class NodeMissingException(Exception):
    """Raised when a node with the given node_id is missing."""

    def __init__(self, message='Node with given node_id is missing'):
        super().__init__(message)


class InvalidPathException(Exception):
    """Raised when a file path does not exist."""

    def __init__(self, message='No such a path'):
        super().__init__(message)


class InvalidSparkInputException(Exception):
    """Raised when an unsupported file extension is provided."""

    def __init__(self, message='Invalid spark input. Supported file extensions: .csv, .json, .parquet'):
        super().__init__(message)


class InvalidInputTypeException(Exception):
    """Raised when an unsupported input type is provided."""

    def __init__(self, message='Input type is not supported. Valid options: ["file", "session"]'):
        super().__init__(message)
