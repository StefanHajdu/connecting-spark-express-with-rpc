class DuplicateSessionException(Exception):
    def __init__(self, message='Duplicate sessions'):
        super().__init__(message)


class LoadNodeRemovalException(Exception):
    def __init__(self, message='Cannot remove load node from plan'):
        super().__init__(message)


class NodeMissingException(Exception):
    def __init__(self, message='Node with given node_id is missing'):
        super().__init__(message)


class InvalidPathException(Exception):
    def __init__(self, message='No such a path'):
        super().__init__(message)


class InvalidSparkInputException(Exception):
    def __init__(self, message='Invalid spark input. Supported file extensions: .csv, .json, .parquet'):
        super().__init__(message)


class InvalidInputTypeException(Exception):
    def __init__(self, message='Input type is not supported. Valid options: ["file", "session"]'):
        super().__init__(message)


class InvalidRemovalException(Exception):
    def __init__(self, message):
        super().__init__(f'Removal of this node breaks the analysis. {message}')


class EmptyException(Exception):
    def __init__(self, message=''):
        super().__init__(message)
