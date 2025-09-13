from abc import ABC, abstractmethod


class NodeQuery(ABC):
    @property
    def default_query(self) -> str:
        return 'select * from {df}'

    @abstractmethod
    def get_query(self) -> str:
        pass


class ExcludedQuery(NodeQuery):
    def get_query(self) -> str:
        return self.default_query


class IncludedQuery(NodeQuery):
    def __init__(self, active: bool, node_specific_query: str):
        self.active = active
        self.node_specific_query = node_specific_query

    def get_query(self) -> str:
        if self.active:
            return self.node_specific_query
        else:
            return self.default_query


def node_query_factory(active: bool, node_input_submitted: bool, node_specific_query: str) -> NodeQuery:
    if active and node_input_submitted:
        return IncludedQuery(active, node_specific_query)
    else:
        return ExcludedQuery()
