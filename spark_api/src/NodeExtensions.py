from enum import Enum
from pathlib import Path

from custom_exceptions import InvalidInpuTypeException
from utils import spark_read_from_path


class InputType(Enum):
    FILE_INPUT = 'file'
    SESSION_INPUT = 'session'


class JoinInputExtension:
    def __init__(self, input_type: str, input_pointer: str):
        if input_type == InputType.FILE_INPUT.value:
            # input_pointer => filesystem path
            self._df = spark_read_from_path(data_type=Path(input_pointer).suffix[1:], path=input_pointer)
        elif input_type == InputType.SESSION_INPUT.value:
            # input_pointer => session_id
            # self._df = sessionPlannerMap.get_session_plan(input_pointer).get_last_spark_node()
            pass
        else:
            raise InvalidInpuTypeException()

        self._schema = self._df.schema.json()

    @property
    def df(self):
        return self._df

    @property
    def schema(self):
        return self._schema
