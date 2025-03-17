class DuplicateSessionException(Exception):
    def __init__(self, message='Duplicate sessions'):
        super().__init__(message)


class InvalidEditException(Exception):
    def __init__(self, message='Invalid sql id provided'):
        super().__init__(message)


class LoadNodeRemovalException(Exception):
    def __init__(self, message='Cannot remove load node from plan'):
        super().__init__(message)


class NodeMissingException(Exception):
    def __init__(self, message='Node with given node_id is missing'):
        super().__init__(message)
