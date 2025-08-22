from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NewSessionResponse(_message.Message):
    __slots__ = ("session_id", "msg")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    msg: str
    def __init__(self, session_id: _Optional[str] = ..., msg: _Optional[str] = ...) -> None: ...

class SparkActionlResponse(_message.Message):
    __slots__ = ("session_id", "msg", "columns", "schema", "count")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    msg: str
    columns: str
    schema: str
    count: int
    def __init__(self, session_id: _Optional[str] = ..., msg: _Optional[str] = ..., columns: _Optional[str] = ..., schema: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ("name", "dtype")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    dtype: str
    def __init__(self, name: _Optional[str] = ..., dtype: _Optional[str] = ...) -> None: ...

class InvalidState(_message.Message):
    __slots__ = ("active", "error_msg")
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    active: bool
    error_msg: str
    def __init__(self, active: bool = ..., error_msg: _Optional[str] = ...) -> None: ...

class SparkTransformResponse(_message.Message):
    __slots__ = ("session_id", "node_id", "invalid_state", "active", "columns")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    INVALID_STATE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    invalid_state: InvalidState
    active: bool
    columns: _containers.RepeatedCompositeFieldContainer[Column]
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., invalid_state: _Optional[_Union[InvalidState, _Mapping]] = ..., active: bool = ..., columns: _Optional[_Iterable[_Union[Column, _Mapping]]] = ...) -> None: ...

class DatasetResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("session_id", "rebuild_recommendation", "cause")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    REBUILD_RECOMMENDATION_FIELD_NUMBER: _ClassVar[int]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    rebuild_recommendation: bool
    cause: str
    def __init__(self, session_id: _Optional[str] = ..., rebuild_recommendation: bool = ..., cause: _Optional[str] = ...) -> None: ...

class NewSessionRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class CsvInput(_message.Message):
    __slots__ = ("delimiter", "include_header", "path")
    DELIMITER_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    delimiter: str
    include_header: bool
    path: str
    def __init__(self, delimiter: _Optional[str] = ..., include_header: bool = ..., path: _Optional[str] = ...) -> None: ...

class JsonInput(_message.Message):
    __slots__ = ("multiline", "path")
    MULTILINE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    multiline: bool
    path: str
    def __init__(self, multiline: bool = ..., path: _Optional[str] = ...) -> None: ...

class ParquetInput(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class LoadDatasetNodeRequest(_message.Message):
    __slots__ = ("session_id", "csv", "json", "parquet")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CSV_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    csv: CsvInput
    json: JsonInput
    parquet: ParquetInput
    def __init__(self, session_id: _Optional[str] = ..., csv: _Optional[_Union[CsvInput, _Mapping]] = ..., json: _Optional[_Union[JsonInput, _Mapping]] = ..., parquet: _Optional[_Union[ParquetInput, _Mapping]] = ...) -> None: ...

class SessionInput(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class PreviewDatasetRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "limit")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    limit: int
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class SummarizeDatasetRequest(_message.Message):
    __slots__ = ("session_id", "node_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ...) -> None: ...

class FilterNodeRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "prev_node_id", "expressions", "matching")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    MATCHING_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    prev_node_id: str
    expressions: _containers.RepeatedScalarFieldContainer[str]
    matching: str
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., prev_node_id: _Optional[str] = ..., expressions: _Optional[_Iterable[str]] = ..., matching: _Optional[str] = ...) -> None: ...

class AddTableNodeRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "prev_node_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    prev_node_id: str
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., prev_node_id: _Optional[str] = ...) -> None: ...

class AddHistogramNodeRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "prev_node_id", "y_axis_col", "order_by", "sort_by", "expression")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_COL_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    prev_node_id: str
    y_axis_col: str
    order_by: str
    sort_by: str
    expression: str
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., prev_node_id: _Optional[str] = ..., y_axis_col: _Optional[str] = ..., order_by: _Optional[str] = ..., sort_by: _Optional[str] = ..., expression: _Optional[str] = ...) -> None: ...

class AddColumnExpression(_message.Message):
    __slots__ = ("expression", "col_name")
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    COL_NAME_FIELD_NUMBER: _ClassVar[int]
    expression: str
    col_name: str
    def __init__(self, expression: _Optional[str] = ..., col_name: _Optional[str] = ...) -> None: ...

class NewColumnNodeRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "prev_node_id", "expressions")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    prev_node_id: str
    expressions: _containers.RepeatedCompositeFieldContainer[AddColumnExpression]
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., prev_node_id: _Optional[str] = ..., expressions: _Optional[_Iterable[_Union[AddColumnExpression, _Mapping]]] = ...) -> None: ...

class JoinParams(_message.Message):
    __slots__ = ("join_relation", "columns_to_keep", "columns_to_add", "prefix_for_added_columns", "join_criteria", "criteria_matching")
    JOIN_RELATION_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_TO_KEEP_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FOR_ADDED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    JOIN_CRITERIA_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_MATCHING_FIELD_NUMBER: _ClassVar[int]
    join_relation: str
    columns_to_keep: _containers.RepeatedScalarFieldContainer[str]
    columns_to_add: _containers.RepeatedScalarFieldContainer[str]
    prefix_for_added_columns: str
    join_criteria: _containers.RepeatedScalarFieldContainer[str]
    criteria_matching: str
    def __init__(self, join_relation: _Optional[str] = ..., columns_to_keep: _Optional[_Iterable[str]] = ..., columns_to_add: _Optional[_Iterable[str]] = ..., prefix_for_added_columns: _Optional[str] = ..., join_criteria: _Optional[_Iterable[str]] = ..., criteria_matching: _Optional[str] = ...) -> None: ...

class JoinNodeRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "prev_node_id", "csv", "json", "parquet", "session", "joinParams")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CSV_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    JOINPARAMS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    prev_node_id: str
    csv: CsvInput
    json: JsonInput
    parquet: ParquetInput
    session: SessionInput
    joinParams: JoinParams
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., prev_node_id: _Optional[str] = ..., csv: _Optional[_Union[CsvInput, _Mapping]] = ..., json: _Optional[_Union[JsonInput, _Mapping]] = ..., parquet: _Optional[_Union[ParquetInput, _Mapping]] = ..., session: _Optional[_Union[SessionInput, _Mapping]] = ..., joinParams: _Optional[_Union[JoinParams, _Mapping]] = ...) -> None: ...

class NodeRemovalRequest(_message.Message):
    __slots__ = ("session_id", "node_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ...) -> None: ...

class NodeToggleRequest(_message.Message):
    __slots__ = ("session_id", "node_id", "toggle")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TOGGLE_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    node_id: str
    toggle: bool
    def __init__(self, session_id: _Optional[str] = ..., node_id: _Optional[str] = ..., toggle: bool = ...) -> None: ...

class LoadFromSessionNodeRequest(_message.Message):
    __slots__ = ("session_id", "input_session_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    input_session_id: str
    def __init__(self, session_id: _Optional[str] = ..., input_session_id: _Optional[str] = ...) -> None: ...

class SessionStatusRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...
