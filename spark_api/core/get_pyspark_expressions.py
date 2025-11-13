import inspect
import json

from pyspark.sql import functions as F

supported_funcs = {
    'new_column': {
        'array': [
            'array',
            'array_contains',
            'get',
            'size',
            'array_join',
            'sort_array',
            'arrays_overlap',
            'slice',
            'concat',
            'array_prepend',
            'array_remove',
            'array_distinct',
            'array_insert',
            'array_intersect',
            'array_union',
            'array_except',
            'array_compact',
            'array_append',
            'shuffle',
            'reverse',
            'flatten',
            'array_repeat',
        ],
        'math': [
            'abs',
            'cbrt',
            'ceil',
            'cos',
            'exp',
            'factorial',
            'floor',
            'isnan',
            'ln',
            'log',
            'pow',
            'rand',
            'round',
            'rtrim',
            'sin',
            'sqrt',
            'tan',
        ],
        'misc': [
            'coalesce',
            'greatest',
            'hash',
            'isnull',
            'least',
            'md5',
            'monotically_increasing_id',
            'sha1',
        ],
        'string': [
            'concat_ws',
            'length',
            'levenshtein',
            'lower',
            'lpad',
            'rpad',
            'ltrim',
            'regexp_extract',
            'regexp_count',
            'regexp_extract_all',
            'regexp_replace',
            'split',
            'substring',
            'trim',
            'upper',
            'base64',
            'is_valid_utf8',
            'make_valid_utf8',
            'endswith',
            'startswith',
        ],
        'date': [
            'add_months',
            'current_date',
            'current_timestamp',
            'date_add',
            'date_sub',
            'date_format',
            'trunc',
            'datediff',
            'dayofweek',
            'dayofyear',
            'dayofmonth',
            'from_utc_timestamp',
            'hour',
            'last_day',
            'minute',
            'month',
            'months_between',
            'to_unix_timestamp',
            'to_utc_timestamp',
            'weekofyear',
            'year',
            'day',
        ],
    }
}


def parse_func_info(func, group, parse_callable):
    sig = inspect.signature(func)
    return {
        'doc': func.__doc__,
        'group': group,
        'args': [
            {'name': arg_name, 'selector': parse_arg_selector(arg_name), **parse_callable(param.annotation)}
            for arg_name, param in sig.parameters.items()
        ],
    }


def parse_arg_selector(name):
    return 'multi' if name == 'cols' else 'single'


def parse_supported(name, func):
    if name in supported_funcs['new_column']['array']:
        return parse_func_info(func, 'array', parse_array_func_type)
    elif name in supported_funcs['new_column']['math']:
        return parse_func_info(func, 'math', parse_math_func_type)
    elif name in supported_funcs['new_column']['misc']:
        return parse_func_info(func, 'misc', parse_misc_func_type)
    elif name in supported_funcs['new_column']['string']:
        return parse_func_info(func, 'string', parse_string_func_type)
    elif name in supported_funcs['new_column']['date']:
        return parse_func_info(func, 'date', parse_date_func_type)


def parse_date_func_type(annotation):
    annotation = str(annotation)
    if annotation == 'ColumnOrName' or annotation == 'typing.Union[pyspark.sql.column.Column, str]':
        return {'type': 'column', 'spark_types': ['date', 'timestamp'], 'custom_input': 'text'}
    elif annotation == "typing.Union[ForwardRef('ColumnOrName'), int]":
        return {'type': 'column', 'spark_types': ['short', 'integer', 'long'], 'custom_input': 'number'}
    elif annotation == "<class 'bool'>":
        return {'type': 'input', 'spark_types': [], 'custom_input': 'checkbox'}
    elif annotation == "<class 'str'>" or annotation == "typing.Optional[ForwardRef('ColumnOrName')]":
        return {'type': 'column', 'spark_types': ['string'], 'custom_input': 'text'}
    else:
        return {'nothing': 'NOTHING'}


def parse_string_func_type(annotation):
    annotation = str(annotation)
    if (
        annotation == 'ColumnOrName'
        or annotation == 'typing.Union[str, pyspark.sql.column.Column]'
        or annotation == 'typing.Union[pyspark.sql.column.Column, str]'
        or annotation == "typing.Optional[ForwardRef('ColumnOrName')]"
    ):
        return {'type': 'column', 'spark_types': ['string'], 'custom_input': 'text'}
    elif annotation == "<class 'str'>" or annotation == 'typing.Optional[str]':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'text'}
    elif annotation == 'typing.Any':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'any'}
    elif (
        annotation == "<class 'int'>"
        or annotation == 'typing.Union[int, pyspark.sql.column.Column, NoneType]'
        or annotation == 'typing.Union[pyspark.sql.column.Column, int]'
        or annotation == "typing.Union[ForwardRef('ColumnOrName'), int]"
        or annotation == 'typing.Optional[int]'
        or annotation == 'typing.Union[pyspark.sql.column.Column, int, NoneType]'
    ):
        return {'type': 'input', 'spark_types': [], 'custom_input': 'number'}
    else:
        return {'nothing': 'NOTHING'}


def parse_math_func_type(annotation):
    annotation = str(annotation)
    if (
        annotation == 'ColumnOrName'
        or annotation == "typing.Optional[ForwardRef('ColumnOrName')]"
        or annotation == "typing.Union[ForwardRef('ColumnOrName'), int]"
        or annotation == "typing.Union[ForwardRef('ColumnOrName'), float]"
        or annotation == 'typing.Union[pyspark.sql.column.Column, int, NoneType]'
    ):
        return {'type': 'column', 'spark_types': ['short', 'integer', 'long', 'float', 'double', 'decimal'], 'custom_input': 'number'}
    elif annotation == "<class 'int'>" or annotation == 'typing.Optional[int]':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'number'}
    elif annotation == 'typing.Any':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'any'}
    elif annotation == "<class 'bool'>":
        return {'type': 'input', 'spark_types': [], 'custom_input': 'checkbox'}
    else:
        return {'nothing': 'NOTHING'}


def parse_misc_func_type(annotation):
    return {
        'type': 'column',
        'spark_types': [
            'short',
            'integer',
            'long',
            'float',
            'double',
            'decimal',
            'string',
            'date',
            'timestamp',
            'array<.*>',
        ],
        'custom_input': 'nan',
    }


def parse_array_func_type(annotation):
    annotation = str(annotation)
    if (
        annotation
        == "typing.Union[ForwardRef('ColumnOrName'), typing.List[ForwardRef('ColumnOrName_')], typing.Tuple[ForwardRef('ColumnOrName_'), ...]]"
        or annotation == 'ColumnOrName'
        or annotation
        == "typing.Union[ForwardRef('ColumnOrName'), typing.Sequence[ForwardRef('ColumnOrName')], typing.Tuple[ForwardRef('ColumnOrName'), ...]]"
    ):
        return {'type': 'column', 'spark_types': ['array<.*>'], 'custom_input': 'nan'}
    elif (
        annotation == "typing.Union[ForwardRef('ColumnOrName'), int]"
        or annotation == 'typing.Union[pyspark.sql.column.Column, int, NoneType]'
    ):
        return {'type': 'column', 'spark_types': ['short', 'integer', 'long', 'float', 'double', 'decimal'], 'custom_input': 'number'}
    elif annotation == "<class 'str'>" or annotation == 'typing.Optional[str]':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'text'}
    elif annotation == 'typing.Any':
        return {'type': 'input', 'spark_types': [], 'custom_input': 'any'}
    elif annotation == "<class 'bool'>":
        return {'type': 'input', 'spark_types': [], 'custom_input': 'checkbox'}
    else:
        return {'nothing': 'NOTHING'}


funcs = inspect.getmembers(F, inspect.isfunction)
spark_funcs_config = {name: parse_supported(name, func) for name, func in inspect.getmembers(F, inspect.isfunction)}
spark_funcs_config = {k: v for k, v in spark_funcs_config.items() if v is not None}

with open('../data/spark_funcs_config.json', 'w') as f:
    json.dump(spark_funcs_config, f)
