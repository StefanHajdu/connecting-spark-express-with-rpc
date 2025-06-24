from abc import ABC, abstractmethod
from enum import Enum

import sparkapi_pb2

import spark_session_init
from utils import load_data_for_spark


class InputType(Enum):
    FILE_INPUT = 'file'
    SESSION_INPUT = 'session'


class NodeExtension(ABC):
    @property
    @abstractmethod
    def df(self) -> str:
        pass

    @property
    @abstractmethod
    def schema(self) -> str:
        pass

    @property
    def query(self) -> str:
        return 'select * from {df}'


class OtherDataframe(NodeExtension):
    def __init__(
        self,
        input_metadata: sparkapi_pb2.CsvInput | sparkapi_pb2.JsonInput | sparkapi_pb2.ParquetInput | sparkapi_pb2.SessionInput,
    ):
        if isinstance(input_metadata, sparkapi_pb2.SessionInput):
            # join with session
            input_session = spark_session_init.clientSessionTable.get_session(input_metadata.session_id)
            self._df = input_session.plan.get_last_spark_node().df
        else:
            # join with dataset
            self._df = load_data_for_spark(input_metadata=input_metadata)

    @property
    def df(self):
        return self._df

    @property
    def schema(self):
        return self.df.schema.json()
