from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import spark_session_init
from custom_exceptions import InvalidInputTypeException
from utils import spark_read_from_path


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
    def __init__(self, input_type: str, input_pointer: str):
        if input_type == InputType.FILE_INPUT.value:
            # input_pointer == filesystem path
            self._df = spark_read_from_path(data_type=Path(input_pointer).suffix[1:], path=input_pointer)
        elif input_type == InputType.SESSION_INPUT.value:
            # input_pointer == session_id
            self._df = spark_session_init.sessionPlannerMap.get_session_plan(input_pointer).get_last_spark_node().df  # noqa: B009
        else:
            raise InvalidInputTypeException()

    @property
    def df(self):
        return self._df

    @property
    def schema(self):
        return self.df.schema.json()
