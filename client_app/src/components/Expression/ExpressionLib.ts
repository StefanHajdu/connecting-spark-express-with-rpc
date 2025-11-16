import type { Group, Arg } from "./Expression.svelte";

export interface Expression {
  doc: string;
  group: Group;
  args: Arg[];
}

interface NamedExpression {
  [name: string]: Expression;
}

export const exprs: NamedExpression = {
  abs: {
    doc: '\n    Mathematical Function: Computes the absolute value of the given column or expression.\n\n    .. versionadded:: 1.3.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        The target column or expression to compute the absolute value on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column object representing the absolute value of the input.\n\n    Examples\n    --------\n    Example 1: Compute the absolute value of a long column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(-1,), (-2,), (-3,), (None,)], ["value"])\n    >>> df.select("*", sf.abs(df.value)).show()\n    +-----+----------+\n    |value|abs(value)|\n    +-----+----------+\n    |   -1|         1|\n    |   -2|         2|\n    |   -3|         3|\n    | NULL|      NULL|\n    +-----+----------+\n\n    Example 2: Compute the absolute value of a double column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(-1.5,), (-2.5,), (None,), (float("nan"),)], ["value"])\n    >>> df.select("*", sf.abs(df.value)).show()\n    +-----+----------+\n    |value|abs(value)|\n    +-----+----------+\n    | -1.5|       1.5|\n    | -2.5|       2.5|\n    | NULL|      NULL|\n    |  NaN|       NaN|\n    +-----+----------+\n\n    Example 3: Compute the absolute value of an expression\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(1, 1), (2, -2), (3, 3)], ["id", "value"])\n    >>> df.select("*", sf.abs(df.id - df.value)).show()\n    +---+-----+-----------------+\n    | id|value|abs((id - value))|\n    +---+-----+-----------------+\n    |  1|    1|                0|\n    |  2|   -2|                4|\n    |  3|    3|                0|\n    +---+-----+-----------------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  add_months: {
    doc: "\n    Returns the date that is `months` months after `start`. If `months` is a negative value\n    then these amount of months will be deducted from the `start`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    start : :class:`~pyspark.sql.Column` or column name\n        date column to work on.\n    months : :class:`~pyspark.sql.Column` or column name or int\n        how many months after the given date to calculate.\n        Accepts negative value as well to calculate backwards.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        a date after/before given number of months.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.dateadd`\n    :meth:`pyspark.sql.functions.date_add`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08', 2,)], 'struct<dt:string,a:int>')\n    >>> df.select('*', sf.add_months(df.dt, 1)).show()\n    +----------+---+-----------------+\n    |        dt|  a|add_months(dt, 1)|\n    +----------+---+-----------------+\n    |2015-04-08|  2|       2015-05-08|\n    +----------+---+-----------------+\n\n    >>> df.select('*', sf.add_months('dt', 'a')).show()\n    +----------+---+-----------------+\n    |        dt|  a|add_months(dt, a)|\n    +----------+---+-----------------+\n    |2015-04-08|  2|       2015-06-08|\n    +----------+---+-----------------+\n\n    >>> df.select('*', sf.add_months('dt', sf.lit(-1))).show()\n    +----------+---+------------------+\n    |        dt|  a|add_months(dt, -1)|\n    +----------+---+------------------+\n    |2015-04-08|  2|        2015-03-08|\n    +----------+---+------------------+\n    ",
    group: "date",
    args: [
      {
        name: "start",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "months",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long"],
        custom_input: "number",
      },
    ],
  },
  array: {
    doc: '\n    Collection function: Creates a new array column from the input columns or column names.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols : :class:`~pyspark.sql.Column` or str\n        Column names or :class:`~pyspark.sql.Column` objects that have the same data type.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new Column of array type, where each value is an array containing the corresponding values\n        from the input columns.\n\n    Examples\n    --------\n    Example 1: Basic usage of array function with column names.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("Alice", "doctor"), ("Bob", "engineer")],\n    ...     ("name", "occupation"))\n    >>> df.select(sf.array(\'name\', \'occupation\')).show()\n    +-----------------------+\n    |array(name, occupation)|\n    +-----------------------+\n    |        [Alice, doctor]|\n    |        [Bob, engineer]|\n    +-----------------------+\n\n    Example 2: Usage of array function with Column objects.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("Alice", "doctor"), ("Bob", "engineer")],\n    ...     ("name", "occupation"))\n    >>> df.select(sf.array(df.name, df.occupation)).show()\n    +-----------------------+\n    |array(name, occupation)|\n    +-----------------------+\n    |        [Alice, doctor]|\n    |        [Bob, engineer]|\n    +-----------------------+\n\n    Example 3: Single argument as list of column names.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("Alice", "doctor"), ("Bob", "engineer")],\n    ...     ("name", "occupation"))\n    >>> df.select(sf.array([\'name\', \'occupation\'])).show()\n    +-----------------------+\n    |array(name, occupation)|\n    +-----------------------+\n    |        [Alice, doctor]|\n    |        [Bob, engineer]|\n    +-----------------------+\n\n    Example 4: Usage of array function with columns of different types.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(\n    ...     [("Alice", 2, 22.2), ("Bob", 5, 36.1)],\n    ...     ("name", "age", "weight"))\n    >>> df.select(sf.array([\'age\', \'weight\'])).show()\n    +------------------+\n    |array(age, weight)|\n    +------------------+\n    |       [2.0, 22.2]|\n    |       [5.0, 36.1]|\n    +------------------+\n\n    Example 5: array function with a column containing null values.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("Alice", None), ("Bob", "engineer")],\n    ...     ("name", "occupation"))\n    >>> df.select(sf.array(\'name\', \'occupation\')).show()\n    +-----------------------+\n    |array(name, occupation)|\n    +-----------------------+\n    |          [Alice, NULL]|\n    |        [Bob, engineer]|\n    +-----------------------+\n    ',
    group: "array",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  array_append: {
    doc: '\n    Array function: returns a new array column by appending `value` to the existing array `col`.\n\n    .. versionadded:: 3.4.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The name of the column containing the array.\n    value :\n        A literal value, or a :class:`~pyspark.sql.Column` expression to be appended to the array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new array column with `value` appended to the original array.\n\n    Notes\n    -----\n    Supports Spark Connect.\n\n    Examples\n    --------\n    Example 1: Appending a column value to an array column\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2="c")])\n    >>> df.select(sf.array_append(df.c1, df.c2)).show()\n    +--------------------+\n    |array_append(c1, c2)|\n    +--------------------+\n    |        [b, a, c, c]|\n    +--------------------+\n\n    Example 2: Appending a numeric value to an array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], [\'data\'])\n    >>> df.select(sf.array_append(df.data, 4)).show()\n    +---------------------+\n    |array_append(data, 4)|\n    +---------------------+\n    |         [1, 2, 3, 4]|\n    +---------------------+\n\n    Example 3: Appending a null value to an array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], [\'data\'])\n    >>> df.select(sf.array_append(df.data, None)).show()\n    +------------------------+\n    |array_append(data, NULL)|\n    +------------------------+\n    |         [1, 2, 3, NULL]|\n    +------------------------+\n\n    Example 4: Appending a value to a NULL array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField("data", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([(None,)], schema=schema)\n    >>> df.select(sf.array_append(df.data, 4)).show()\n    +---------------------+\n    |array_append(data, 4)|\n    +---------------------+\n    |                 NULL|\n    +---------------------+\n\n    Example 5: Appending a value to an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField("data", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([],)], schema=schema)\n    >>> df.select(sf.array_append(df.data, 1)).show()\n    +---------------------+\n    |array_append(data, 1)|\n    +---------------------+\n    |                  [1]|\n    +---------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "value",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "any",
      },
    ],
  },
  array_compact: {
    doc: "\n    Array function: removes null values from the array.\n\n    .. versionadded:: 3.4.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        name of column or expression\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that is an array excluding the null values from the input column.\n\n    Notes\n    -----\n    Supports Spark Connect.\n\n    Examples\n    --------\n    Example 1: Removing null values from a simple array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, None, 2, 3],)], ['data'])\n    >>> df.select(sf.array_compact(df.data)).show()\n    +-------------------+\n    |array_compact(data)|\n    +-------------------+\n    |          [1, 2, 3]|\n    +-------------------+\n\n    Example 2: Removing null values from multiple arrays\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, None, 2, 3],), ([4, 5, None, 4],)], ['data'])\n    >>> df.select(sf.array_compact(df.data)).show()\n    +-------------------+\n    |array_compact(data)|\n    +-------------------+\n    |          [1, 2, 3]|\n    |          [4, 5, 4]|\n    +-------------------+\n\n    Example 3: Removing null values from an array with all null values\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> schema = StructType([\n    ...   StructField(\"data\", ArrayType(StringType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([None, None, None],)], schema)\n    >>> df.select(sf.array_compact(df.data)).show()\n    +-------------------+\n    |array_compact(data)|\n    +-------------------+\n    |                 []|\n    +-------------------+\n\n    Example 4: Removing null values from an array with no null values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], ['data'])\n    >>> df.select(sf.array_compact(df.data)).show()\n    +-------------------+\n    |array_compact(data)|\n    +-------------------+\n    |          [1, 2, 3]|\n    +-------------------+\n\n    Example 5: Removing null values from an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> schema = StructType([\n    ...   StructField(\"data\", ArrayType(StringType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([],)], schema)\n    >>> df.select(sf.array_compact(df.data)).show()\n    +-------------------+\n    |array_compact(data)|\n    +-------------------+\n    |                 []|\n    +-------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  array_contains: {
    doc: '\n    Collection function: This function returns a boolean indicating whether the array\n    contains the given value, returning null if the array is null, true if the array\n    contains the given value, and false otherwise.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The target column containing the arrays.\n    value :\n        The value or column to check for in the array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new Column of Boolean type, where each value indicates whether the corresponding array\n        from the input column contains the specified value.\n\n    Examples\n    --------\n    Example 1: Basic usage of array_contains function.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"],), ([],)], [\'data\'])\n    >>> df.select(sf.array_contains(df.data, "a")).show()\n    +-----------------------+\n    |array_contains(data, a)|\n    +-----------------------+\n    |                   true|\n    |                  false|\n    +-----------------------+\n\n    Example 2: Usage of array_contains function with a column.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"], "c"),\n    ...                            (["c", "d", "e"], "d"),\n    ...                            (["e", "a", "c"], "b")], ["data", "item"])\n    >>> df.select(sf.array_contains(df.data, sf.col("item"))).show()\n    +--------------------------+\n    |array_contains(data, item)|\n    +--------------------------+\n    |                      true|\n    |                      true|\n    |                     false|\n    +--------------------------+\n\n    Example 3: Attempt to use array_contains function with a null array.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(None,), (["a", "b", "c"],)], [\'data\'])\n    >>> df.select(sf.array_contains(df.data, "a")).show()\n    +-----------------------+\n    |array_contains(data, a)|\n    +-----------------------+\n    |                   NULL|\n    |                   true|\n    +-----------------------+\n\n    Example 4: Usage of array_contains with an array column containing null values.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", None, "c"],)], [\'data\'])\n    >>> df.select(sf.array_contains(df.data, "a")).show()\n    +-----------------------+\n    |array_contains(data, a)|\n    +-----------------------+\n    |                   true|\n    +-----------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "value",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "any",
      },
    ],
  },
  array_distinct: {
    doc: "\n    Array function: removes duplicate values from the array.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        name of column or expression\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that is an array of unique values from the input column.\n\n    Examples\n    --------\n    Example 1: Removing duplicate values from a simple array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3, 2],)], ['data'])\n    >>> df.select(sf.array_distinct(df.data)).show()\n    +--------------------+\n    |array_distinct(data)|\n    +--------------------+\n    |           [1, 2, 3]|\n    +--------------------+\n\n    Example 2: Removing duplicate values from multiple arrays\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3, 2],), ([4, 5, 5, 4],)], ['data'])\n    >>> df.select(sf.array_distinct(df.data)).show()\n    +--------------------+\n    |array_distinct(data)|\n    +--------------------+\n    |           [1, 2, 3]|\n    |              [4, 5]|\n    +--------------------+\n\n    Example 3: Removing duplicate values from an array with all identical values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 1, 1],)], ['data'])\n    >>> df.select(sf.array_distinct(df.data)).show()\n    +--------------------+\n    |array_distinct(data)|\n    +--------------------+\n    |                 [1]|\n    +--------------------+\n\n    Example 4: Removing duplicate values from an array with no duplicate values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], ['data'])\n    >>> df.select(sf.array_distinct(df.data)).show()\n    +--------------------+\n    |array_distinct(data)|\n    +--------------------+\n    |           [1, 2, 3]|\n    +--------------------+\n\n    Example 5: Removing duplicate values from an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField(\"data\", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([],)], schema)\n    >>> df.select(sf.array_distinct(df.data)).show()\n    +--------------------+\n    |array_distinct(data)|\n    +--------------------+\n    |                  []|\n    +--------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  array_except: {
    doc: '\n    Array function: returns a new array containing the elements present in col1 but not in col2,\n    without duplicates.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col1 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the first array.\n    col2 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the second array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new array containing the elements present in col1 but not in col2.\n\n    Notes\n    -----\n    This function does not preserve the order of the elements in the input arrays.\n\n    Examples\n    --------\n    Example 1: Basic usage\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["c", "d", "a", "f"])])\n    >>> df.select(sf.array_except(df.c1, df.c2)).show()\n    +--------------------+\n    |array_except(c1, c2)|\n    +--------------------+\n    |                 [b]|\n    +--------------------+\n\n    Example 2: Except with no common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["d", "e", "f"])])\n    >>> df.select(sf.sort_array(sf.array_except(df.c1, df.c2))).show()\n    +--------------------------------------+\n    |sort_array(array_except(c1, c2), true)|\n    +--------------------------------------+\n    |                             [a, b, c]|\n    +--------------------------------------+\n\n    Example 3: Except with all common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", "c"], c2=["a", "b", "c"])])\n    >>> df.select(sf.array_except(df.c1, df.c2)).show()\n    +--------------------+\n    |array_except(c1, c2)|\n    +--------------------+\n    |                  []|\n    +--------------------+\n\n    Example 4: Except with null values\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", None], c2=["a", None, "c"])])\n    >>> df.select(sf.array_except(df.c1, df.c2)).show()\n    +--------------------+\n    |array_except(c1, c2)|\n    +--------------------+\n    |                 [b]|\n    +--------------------+\n\n    Example 5: Except with empty arrays\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> data = [Row(c1=[], c2=["a", "b", "c"])]\n    >>> schema = StructType([\n    ...   StructField("c1", ArrayType(StringType()), True),\n    ...   StructField("c2", ArrayType(StringType()), True)\n    ... ])\n    >>> df = spark.createDataFrame(data, schema)\n    >>> df.select(sf.array_except(df.c1, df.c2)).show()\n    +--------------------+\n    |array_except(c1, c2)|\n    +--------------------+\n    |                  []|\n    +--------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col1",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "col2",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  array_insert: {
    doc: "\n    Array function: Inserts an item into a given array at a specified array index.\n    Array indices start at 1, or start from the end if index is negative.\n    Index above array size appends the array, or prepends the array if index is negative,\n    with 'null' elements.\n\n    .. versionadded:: 3.4.0\n\n    Parameters\n    ----------\n    arr : :class:`~pyspark.sql.Column` or str\n        name of column containing an array\n    pos : :class:`~pyspark.sql.Column` or str or int\n        name of Numeric type column indicating position of insertion\n        (starting at index 1, negative position is a start from the back of the array)\n    value :\n        a literal value, or a :class:`~pyspark.sql.Column` expression.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        an array of values, including the new specified value\n\n    Notes\n    -----\n    Supports Spark Connect.\n\n    Examples\n    --------\n    Example 1: Inserting a value at a specific position\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(['a', 'b', 'c'],)], ['data'])\n    >>> df.select(sf.array_insert(df.data, 2, 'd')).show()\n    +------------------------+\n    |array_insert(data, 2, d)|\n    +------------------------+\n    |            [a, d, b, c]|\n    +------------------------+\n\n    Example 2: Inserting a value at a negative position\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(['a', 'b', 'c'],)], ['data'])\n    >>> df.select(sf.array_insert(df.data, -2, 'd')).show()\n    +-------------------------+\n    |array_insert(data, -2, d)|\n    +-------------------------+\n    |             [a, b, d, c]|\n    +-------------------------+\n\n    Example 3: Inserting a value at a position greater than the array size\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(['a', 'b', 'c'],)], ['data'])\n    >>> df.select(sf.array_insert(df.data, 5, 'e')).show()\n    +------------------------+\n    |array_insert(data, 5, e)|\n    +------------------------+\n    |      [a, b, c, NULL, e]|\n    +------------------------+\n\n    Example 4: Inserting a NULL value\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(['a', 'b', 'c'],)], ['data'])\n    >>> df.select(sf.array_insert(df.data, 2, sf.lit(None))).show()\n    +---------------------------+\n    |array_insert(data, 2, NULL)|\n    +---------------------------+\n    |            [a, NULL, b, c]|\n    +---------------------------+\n\n    Example 5: Inserting a value into a NULL array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([StructField(\"data\", ArrayType(IntegerType()), True)])\n    >>> df = spark.createDataFrame([(None,)], schema=schema)\n    >>> df.select(sf.array_insert(df.data, 1, 5)).show()\n    +------------------------+\n    |array_insert(data, 1, 5)|\n    +------------------------+\n    |                    NULL|\n    +------------------------+\n    ",
    group: "array",
    args: [
      {
        name: "arr",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "pos",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "value",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "any",
      },
    ],
  },
  array_intersect: {
    doc: '\n    Array function: returns a new array containing the intersection of elements in col1 and col2,\n    without duplicates.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col1 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the first array.\n    col2 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the second array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new array containing the intersection of elements in col1 and col2.\n\n    Notes\n    -----\n    This function does not preserve the order of the elements in the input arrays.\n\n    Examples\n    --------\n    Example 1: Basic usage\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["c", "d", "a", "f"])])\n    >>> df.select(sf.sort_array(sf.array_intersect(df.c1, df.c2))).show()\n    +-----------------------------------------+\n    |sort_array(array_intersect(c1, c2), true)|\n    +-----------------------------------------+\n    |                                   [a, c]|\n    +-----------------------------------------+\n\n    Example 2: Intersection with no common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["d", "e", "f"])])\n    >>> df.select(sf.array_intersect(df.c1, df.c2)).show()\n    +-----------------------+\n    |array_intersect(c1, c2)|\n    +-----------------------+\n    |                     []|\n    +-----------------------+\n\n    Example 3: Intersection with all common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", "c"], c2=["a", "b", "c"])])\n    >>> df.select(sf.sort_array(sf.array_intersect(df.c1, df.c2))).show()\n    +-----------------------------------------+\n    |sort_array(array_intersect(c1, c2), true)|\n    +-----------------------------------------+\n    |                                [a, b, c]|\n    +-----------------------------------------+\n\n    Example 4: Intersection with null values\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", None], c2=["a", None, "c"])])\n    >>> df.select(sf.sort_array(sf.array_intersect(df.c1, df.c2))).show()\n    +-----------------------------------------+\n    |sort_array(array_intersect(c1, c2), true)|\n    +-----------------------------------------+\n    |                                [NULL, a]|\n    +-----------------------------------------+\n\n    Example 5: Intersection with empty arrays\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> data = [Row(c1=[], c2=["a", "b", "c"])]\n    >>> schema = StructType([\n    ...   StructField("c1", ArrayType(StringType()), True),\n    ...   StructField("c2", ArrayType(StringType()), True)\n    ... ])\n    >>> df = spark.createDataFrame(data, schema)\n    >>> df.select(sf.array_intersect(df.c1, df.c2)).show()\n    +-----------------------+\n    |array_intersect(c1, c2)|\n    +-----------------------+\n    |                     []|\n    +-----------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col1",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "col2",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  array_join: {
    doc: '\n    Array function: Returns a string column by concatenating the elements of the input\n    array column using the delimiter. Null values within the array can be replaced with\n    a specified string through the null_replacement argument. If null_replacement is\n    not set, null values are ignored.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The input column containing the arrays to be joined.\n    delimiter : str\n        The string to be used as the delimiter when joining the array elements.\n    null_replacement : str, optional\n        The string to replace null values within the array. If not set, null values are ignored.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column of string type, where each value is the result of joining the corresponding\n        array from the input column.\n\n    Examples\n    --------\n    Example 1: Basic usage of array_join function.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"],), (["a", "b"],)], [\'data\'])\n    >>> df.select(sf.array_join(df.data, ",")).show()\n    +-------------------+\n    |array_join(data, ,)|\n    +-------------------+\n    |              a,b,c|\n    |                a,b|\n    +-------------------+\n\n    Example 2: Usage of array_join function with null_replacement argument.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", None, "c"],)], [\'data\'])\n    >>> df.select(sf.array_join(df.data, ",", "NULL")).show()\n    +-------------------------+\n    |array_join(data, ,, NULL)|\n    +-------------------------+\n    |                 a,NULL,c|\n    +-------------------------+\n\n    Example 3: Usage of array_join function without null_replacement argument.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", None, "c"],)], [\'data\'])\n    >>> df.select(sf.array_join(df.data, ",")).show()\n    +-------------------+\n    |array_join(data, ,)|\n    +-------------------+\n    |                a,c|\n    +-------------------+\n\n    Example 4: Usage of array_join function with an array that is null.\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import StructType, StructField, ArrayType, StringType\n    >>> schema = StructType([StructField("data", ArrayType(StringType()), True)])\n    >>> df = spark.createDataFrame([(None,)], schema)\n    >>> df.select(sf.array_join(df.data, ",")).show()\n    +-------------------+\n    |array_join(data, ,)|\n    +-------------------+\n    |               NULL|\n    +-------------------+\n\n    Example 5: Usage of array_join function with an array containing only null values.\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import StructType, StructField, ArrayType, StringType\n    >>> schema = StructType([StructField("data", ArrayType(StringType()), True)])\n    >>> df = spark.createDataFrame([([None, None],)], schema)\n    >>> df.select(sf.array_join(df.data, ",", "NULL")).show()\n    +-------------------------+\n    |array_join(data, ,, NULL)|\n    +-------------------------+\n    |                NULL,NULL|\n    +-------------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "delimiter",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "text",
      },
      {
        name: "null_replacement",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "text",
      },
    ],
  },
  array_prepend: {
    doc: '\n    Array function: Returns an array containing the given element as\n    the first element and the rest of the elements from the original array.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        name of column containing array\n    value :\n        a literal value, or a :class:`~pyspark.sql.Column` expression.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        an array with the given value prepended.\n\n    Examples\n    --------\n    Example 1: Prepending a column value to an array column\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2="c")])\n    >>> df.select(sf.array_prepend(df.c1, df.c2)).show()\n    +---------------------+\n    |array_prepend(c1, c2)|\n    +---------------------+\n    |         [c, b, a, c]|\n    +---------------------+\n\n    Example 2: Prepending a numeric value to an array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], [\'data\'])\n    >>> df.select(sf.array_prepend(df.data, 4)).show()\n    +----------------------+\n    |array_prepend(data, 4)|\n    +----------------------+\n    |          [4, 1, 2, 3]|\n    +----------------------+\n\n    Example 3: Prepending a null value to an array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], [\'data\'])\n    >>> df.select(sf.array_prepend(df.data, None)).show()\n    +-------------------------+\n    |array_prepend(data, NULL)|\n    +-------------------------+\n    |          [NULL, 1, 2, 3]|\n    +-------------------------+\n\n    Example 4: Prepending a value to a NULL array column\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField("data", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([(None,)], schema=schema)\n    >>> df.select(sf.array_prepend(df.data, 4)).show()\n    +----------------------+\n    |array_prepend(data, 4)|\n    +----------------------+\n    |                  NULL|\n    +----------------------+\n\n    Example 5: Prepending a value to an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField("data", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([],)], schema=schema)\n    >>> df.select(sf.array_prepend(df.data, 1)).show()\n    +----------------------+\n    |array_prepend(data, 1)|\n    +----------------------+\n    |                   [1]|\n    +----------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "value",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "any",
      },
    ],
  },
  array_remove: {
    doc: "\n    Array function: Remove all elements that equal to element from the given array.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        name of column containing array\n    element :\n        element or a :class:`~pyspark.sql.Column` expression to be removed from the array\n\n        .. versionchanged:: 4.0.0\n            `element` now also accepts a Column type.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that is an array excluding the given value from the input column.\n\n    Examples\n    --------\n    Example 1: Removing a specific value from a simple array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3, 1, 1],)], ['data'])\n    >>> df.select(sf.array_remove(df.data, 1)).show()\n    +---------------------+\n    |array_remove(data, 1)|\n    +---------------------+\n    |               [2, 3]|\n    +---------------------+\n\n    Example 2: Removing a specific value from multiple arrays\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3, 1, 1],), ([4, 5, 5, 4],)], ['data'])\n    >>> df.select(sf.array_remove(df.data, 5)).show()\n    +---------------------+\n    |array_remove(data, 5)|\n    +---------------------+\n    |      [1, 2, 3, 1, 1]|\n    |               [4, 4]|\n    +---------------------+\n\n    Example 3: Removing a value that does not exist in the array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],)], ['data'])\n    >>> df.select(sf.array_remove(df.data, 4)).show()\n    +---------------------+\n    |array_remove(data, 4)|\n    +---------------------+\n    |            [1, 2, 3]|\n    +---------------------+\n\n    Example 4: Removing a value from an array with all identical values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 1, 1],)], ['data'])\n    >>> df.select(sf.array_remove(df.data, 1)).show()\n    +---------------------+\n    |array_remove(data, 1)|\n    +---------------------+\n    |                   []|\n    +---------------------+\n\n    Example 5: Removing a value from an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField(\"data\", ArrayType(IntegerType()), True)\n    ... ])\n    >>> df = spark.createDataFrame([([],)], schema)\n    >>> df.select(sf.array_remove(df.data, 1)).show()\n    +---------------------+\n    |array_remove(data, 1)|\n    +---------------------+\n    |                   []|\n    +---------------------+\n\n    Example 6: Removing a column's value from a simple array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3, 1, 1], 1)], ['data', 'col'])\n    >>> df.select(sf.array_remove(df.data, df.col)).show()\n    +-----------------------+\n    |array_remove(data, col)|\n    +-----------------------+\n    |                 [2, 3]|\n    +-----------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "element",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "any",
      },
    ],
  },
  array_repeat: {
    doc: "\n    Array function: creates an array containing a column repeated count times.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The name of the column or an expression that represents the element to be repeated.\n    count : :class:`~pyspark.sql.Column` or str or int\n        The name of the column, an expression,\n        or an integer that represents the number of times to repeat the element.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that contains an array of repeated elements.\n\n    Examples\n    --------\n    Example 1: Usage with string\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('ab',)], ['data'])\n    >>> df.select(sf.array_repeat(df.data, 3)).show()\n    +---------------------+\n    |array_repeat(data, 3)|\n    +---------------------+\n    |         [ab, ab, ab]|\n    +---------------------+\n\n    Example 2: Usage with integer\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(3,)], ['data'])\n    >>> df.select(sf.array_repeat(df.data, 2)).show()\n    +---------------------+\n    |array_repeat(data, 2)|\n    +---------------------+\n    |               [3, 3]|\n    +---------------------+\n\n    Example 3: Usage with array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(['apple', 'banana'],)], ['data'])\n    >>> df.select(sf.array_repeat(df.data, 2)).show(truncate=False)\n    +----------------------------------+\n    |array_repeat(data, 2)             |\n    +----------------------------------+\n    |[[apple, banana], [apple, banana]]|\n    +----------------------------------+\n\n    Example 4: Usage with null\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import IntegerType, StructType, StructField\n    >>> schema = StructType([\n    ...   StructField(\"data\", IntegerType(), True)\n    ... ])\n    >>> df = spark.createDataFrame([(None, )], schema=schema)\n    >>> df.select(sf.array_repeat(df.data, 3)).show()\n    +---------------------+\n    |array_repeat(data, 3)|\n    +---------------------+\n    |   [NULL, NULL, NULL]|\n    +---------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "count",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  array_union: {
    doc: '\n    Array function: returns a new array containing the union of elements in col1 and col2,\n    without duplicates.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col1 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the first array.\n    col2 : :class:`~pyspark.sql.Column` or str\n        Name of column containing the second array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new array containing the union of elements in col1 and col2.\n\n    Notes\n    -----\n    This function does not preserve the order of the elements in the input arrays.\n\n    Examples\n    --------\n    Example 1: Basic usage\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["c", "d", "a", "f"])])\n    >>> df.select(sf.sort_array(sf.array_union(df.c1, df.c2))).show()\n    +-------------------------------------+\n    |sort_array(array_union(c1, c2), true)|\n    +-------------------------------------+\n    |                      [a, b, c, d, f]|\n    +-------------------------------------+\n\n    Example 2: Union with no common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["b", "a", "c"], c2=["d", "e", "f"])])\n    >>> df.select(sf.sort_array(sf.array_union(df.c1, df.c2))).show()\n    +-------------------------------------+\n    |sort_array(array_union(c1, c2), true)|\n    +-------------------------------------+\n    |                   [a, b, c, d, e, f]|\n    +-------------------------------------+\n\n    Example 3: Union with all common elements\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", "c"], c2=["a", "b", "c"])])\n    >>> df.select(sf.sort_array(sf.array_union(df.c1, df.c2))).show()\n    +-------------------------------------+\n    |sort_array(array_union(c1, c2), true)|\n    +-------------------------------------+\n    |                            [a, b, c]|\n    +-------------------------------------+\n\n    Example 4: Union with null values\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> df = spark.createDataFrame([Row(c1=["a", "b", None], c2=["a", None, "c"])])\n    >>> df.select(sf.sort_array(sf.array_union(df.c1, df.c2))).show()\n    +-------------------------------------+\n    |sort_array(array_union(c1, c2), true)|\n    +-------------------------------------+\n    |                      [NULL, a, b, c]|\n    +-------------------------------------+\n\n    Example 5: Union with empty arrays\n\n    >>> from pyspark.sql import Row, functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> data = [Row(c1=[], c2=["a", "b", "c"])]\n    >>> schema = StructType([\n    ...   StructField("c1", ArrayType(StringType()), True),\n    ...   StructField("c2", ArrayType(StringType()), True)\n    ... ])\n    >>> df = spark.createDataFrame(data, schema)\n    >>> df.select(sf.sort_array(sf.array_union(df.c1, df.c2))).show()\n    +-------------------------------------+\n    |sort_array(array_union(c1, c2), true)|\n    +-------------------------------------+\n    |                            [a, b, c]|\n    +-------------------------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col1",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "col2",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  arrays_overlap: {
    doc: '\n    Collection function: This function returns a boolean column indicating if the input arrays\n    have common non-null elements, returning true if they do, null if the arrays do not contain\n    any common elements but are not empty and at least one of them contains a null element,\n    and false otherwise.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    a1, a2 : :class:`~pyspark.sql.Column` or str\n        The names of the columns that contain the input arrays.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new Column of Boolean type, where each value indicates whether the corresponding arrays\n        from the input columns contain any common elements.\n\n    Examples\n    --------\n    Example 1: Basic usage of arrays_overlap function.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b"], ["b", "c"]), (["a"], ["b", "c"])], [\'x\', \'y\'])\n    >>> df.select(sf.arrays_overlap(df.x, df.y)).show()\n    +--------------------+\n    |arrays_overlap(x, y)|\n    +--------------------+\n    |                true|\n    |               false|\n    +--------------------+\n\n    Example 2: Usage of arrays_overlap function with arrays containing null elements.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", None], ["b", None]), (["a"], ["b", "c"])], [\'x\', \'y\'])\n    >>> df.select(sf.arrays_overlap(df.x, df.y)).show()\n    +--------------------+\n    |arrays_overlap(x, y)|\n    +--------------------+\n    |                NULL|\n    |               false|\n    +--------------------+\n\n    Example 3: Usage of arrays_overlap function with arrays that are null.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(None, ["b", "c"]), (["a"], None)], [\'x\', \'y\'])\n    >>> df.select(sf.arrays_overlap(df.x, df.y)).show()\n    +--------------------+\n    |arrays_overlap(x, y)|\n    +--------------------+\n    |                NULL|\n    |                NULL|\n    +--------------------+\n\n    Example 4: Usage of arrays_overlap on arrays with identical elements.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b"], ["a", "b"]), (["a"], ["a"])], [\'x\', \'y\'])\n    >>> df.select(sf.arrays_overlap(df.x, df.y)).show()\n    +--------------------+\n    |arrays_overlap(x, y)|\n    +--------------------+\n    |                true|\n    |                true|\n    +--------------------+\n    ',
    group: "array",
    args: [
      {
        name: "a1",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "a2",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  base64: {
    doc: '\n    Computes the BASE64 encoding of a binary column and returns it as a string column.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        BASE64 encoding of string value.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.unbase64`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["Spark", "PySpark", "Pandas API"], "STRING")\n    >>> df.select("*", sf.base64("value")).show()\n    +----------+----------------+\n    |     value|   base64(value)|\n    +----------+----------------+\n    |     Spark|        U3Bhcms=|\n    |   PySpark|    UHlTcGFyaw==|\n    |Pandas API|UGFuZGFzIEFQSQ==|\n    +----------+----------------+\n    ',
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  cbrt: {
    doc: '\n    Computes the cube-root of the given value.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the column for computed results.\n\n    Examples\n    --------\n    Example 1: Compute the cube-root\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(-8,), (0,), (8,)], ["value"])\n    >>> df.select("*", sf.cbrt(df.value)).show()\n    +-----+-----------+\n    |value|CBRT(value)|\n    +-----+-----------+\n    |   -8|       -2.0|\n    |    0|        0.0|\n    |    8|        2.0|\n    +-----+-----------+\n\n    Example 2: Compute the cube-root of invalid values\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (FLOAT(\'NAN\')), (NULL) AS TAB(value)"\n    ... ).select("*", sf.cbrt("value")).show()\n    +-----+-----------+\n    |value|CBRT(value)|\n    +-----+-----------+\n    |  NaN|        NaN|\n    | NULL|       NULL|\n    +-----+-----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  ceil: {
    doc: "\n    Computes the ceiling of the given value.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        The target column or column name to compute the ceiling on.\n    scale : :class:`~pyspark.sql.Column` or int, optional\n        An optional parameter to control the rounding behavior.\n\n        .. versionadded:: 4.0.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A column for the computed results.\n\n    Examples\n    --------\n    Example 1: Compute the ceiling of a column value\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(1).select(sf.ceil(sf.lit(-0.1))).show()\n    +----------+\n    |CEIL(-0.1)|\n    +----------+\n    |         0|\n    +----------+\n\n    Example 2: Compute the ceiling of a column value with a specified scale\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(1).select(sf.ceil(sf.lit(-0.1), 1)).show()\n    +-------------+\n    |ceil(-0.1, 1)|\n    +-------------+\n    |         -0.1|\n    +-------------+\n    ",
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "scale",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  coalesce: {
    doc: 'Returns the first column that is not null.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols : :class:`~pyspark.sql.Column` or column name\n        list of columns to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        value of the first column that is not null.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(None, None), (1, None), (None, 2)], ("a", "b"))\n    >>> df.show()\n    +----+----+\n    |   a|   b|\n    +----+----+\n    |NULL|NULL|\n    |   1|NULL|\n    |NULL|   2|\n    +----+----+\n\n    >>> df.select(\'*\', sf.coalesce("a", df["b"])).show()\n    +----+----+--------------+\n    |   a|   b|coalesce(a, b)|\n    +----+----+--------------+\n    |NULL|NULL|          NULL|\n    |   1|NULL|             1|\n    |NULL|   2|             2|\n    +----+----+--------------+\n\n    >>> df.select(\'*\', sf.coalesce(df["a"], lit(0.0))).show()\n    +----+----+----------------+\n    |   a|   b|coalesce(a, 0.0)|\n    +----+----+----------------+\n    |NULL|NULL|             0.0|\n    |   1|NULL|             1.0|\n    |NULL|   2|             0.0|\n    +----+----+----------------+\n    ',
    group: "misc",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  concat: {
    doc: "\n    Collection function: Concatenates multiple input columns together into a single column.\n    The function works with strings, numeric, binary and compatible array columns.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols : :class:`~pyspark.sql.Column` or str\n        target column or columns to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        concatenated values. Type of the `Column` depends on input columns' type.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.concat_ws`\n    :meth:`pyspark.sql.functions.array_join` : to concatenate string columns with delimiter\n\n    Examples\n    --------\n    Example 1: Concatenating string columns\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('abcd','123')], ['s', 'd'])\n    >>> df.select(sf.concat(df.s, df.d)).show()\n    +------------+\n    |concat(s, d)|\n    +------------+\n    |     abcd123|\n    +------------+\n\n    Example 2: Concatenating array columns\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2], [3, 4], [5]), ([1, 2], None, [3])], ['a', 'b', 'c'])\n    >>> df.select(sf.concat(df.a, df.b, df.c)).show()\n    +---------------+\n    |concat(a, b, c)|\n    +---------------+\n    |[1, 2, 3, 4, 5]|\n    |           NULL|\n    +---------------+\n\n    Example 3: Concatenating numeric columns\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(1, 2, 3)], ['a', 'b', 'c'])\n    >>> df.select(sf.concat(df.a, df.b, df.c)).show()\n    +---------------+\n    |concat(a, b, c)|\n    +---------------+\n    |            123|\n    +---------------+\n\n    Example 4: Concatenating binary columns\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(bytearray(b'abc'), bytearray(b'def'))], ['a', 'b'])\n    >>> df.select(sf.concat(df.a, df.b)).show()\n    +-------------------+\n    |       concat(a, b)|\n    +-------------------+\n    |[61 62 63 64 65 66]|\n    +-------------------+\n\n    Example 5: Concatenating mixed types of columns\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(1,\"abc\",3,\"def\")], ['a','b','c','d'])\n    >>> df.select(sf.concat(df.a, df.b, df.c, df.d)).show()\n    +------------------+\n    |concat(a, b, c, d)|\n    +------------------+\n    |          1abc3def|\n    +------------------+\n    ",
    group: "array",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  concat_ws: {
    doc: '\n    Concatenates multiple input string columns together into a single string column,\n    using the given separator.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    sep : literal string\n        words separator.\n    cols : :class:`~pyspark.sql.Column` or column name\n        list of columns to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        string of concatenated words.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.concat`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("abcd", "123")], ["s", "d"])\n    >>> df.select("*", sf.concat_ws("-", df.s, "d", sf.lit("xyz"))).show()\n    +----+---+-----------------------+\n    |   s|  d|concat_ws(-, s, d, xyz)|\n    +----+---+-----------------------+\n    |abcd|123|           abcd-123-xyz|\n    +----+---+-----------------------+\n    ',
    group: "string",
    args: [
      {
        name: "sep",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "text",
      },
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  cos: {
    doc: '\n    Computes cosine of the input column.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        angle in radians\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        cosine of the angle, as if computed by `java.lang.Math.cos()`.\n\n    Examples\n    --------\n    Example 1: Compute the cosine\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (PI()), (PI() / 4), (PI() / 16) AS TAB(value)"\n    ... ).select("*", sf.cos("value")).show()\n    +-------------------+------------------+\n    |              value|        COS(value)|\n    +-------------------+------------------+\n    |  3.141592653589...|              -1.0|\n    | 0.7853981633974...|0.7071067811865...|\n    |0.19634954084936...|0.9807852804032...|\n    +-------------------+------------------+\n\n    Example 2: Compute the cosine of invalid values\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (FLOAT(\'NAN\')), (NULL) AS TAB(value)"\n    ... ).select("*", sf.cos("value")).show()\n    +-----+----------+\n    |value|COS(value)|\n    +-----+----------+\n    |  NaN|       NaN|\n    | NULL|      NULL|\n    +-----+----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  current_date: {
    doc: "\n    Returns the current date at the start of query evaluation as a :class:`DateType` column.\n    All calls of current_date within the same query return the same value.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        current date.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.now`\n    :meth:`pyspark.sql.functions.curdate`\n    :meth:`pyspark.sql.functions.current_timestamp`\n    :meth:`pyspark.sql.functions.localtimestamp`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(1).select(sf.current_date()).show() # doctest: +SKIP\n    +--------------+\n    |current_date()|\n    +--------------+\n    |    2022-08-26|\n    +--------------+\n    ",
    group: "date",
    args: [],
  },
  current_timestamp: {
    doc: "\n    Returns the current timestamp at the start of query evaluation as a :class:`TimestampType`\n    column. All calls of current_timestamp within the same query return the same value.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        current date and time.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.now`\n    :meth:`pyspark.sql.functions.curdate`\n    :meth:`pyspark.sql.functions.current_date`\n    :meth:`pyspark.sql.functions.localtimestamp`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(1).select(sf.current_timestamp()).show(truncate=False) # doctest: +SKIP\n    +-----------------------+\n    |current_timestamp()    |\n    +-----------------------+\n    |2022-08-26 21:23:22.716|\n    +-----------------------+\n    ",
    group: "date",
    args: [],
  },
  date_add: {
    doc: "\n    Returns the date that is `days` days after `start`. If `days` is a negative value\n    then these amount of days will be deducted from `start`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    start : :class:`~pyspark.sql.Column` or column name\n        date column to work on.\n    days : :class:`~pyspark.sql.Column` or column name or int\n        how many days after the given date to calculate.\n        Accepts negative value as well to calculate backwards in time.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        a date after/before given number of days.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.dateadd`\n    :meth:`pyspark.sql.functions.date_sub`\n    :meth:`pyspark.sql.functions.datediff`\n    :meth:`pyspark.sql.functions.date_diff`\n    :meth:`pyspark.sql.functions.timestamp_add`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08', 2,)], 'struct<dt:string,a:int>')\n    >>> df.select('*', sf.date_add(df.dt, 1)).show()\n    +----------+---+---------------+\n    |        dt|  a|date_add(dt, 1)|\n    +----------+---+---------------+\n    |2015-04-08|  2|     2015-04-09|\n    +----------+---+---------------+\n\n    >>> df.select('*', sf.date_add('dt', 'a')).show()\n    +----------+---+---------------+\n    |        dt|  a|date_add(dt, a)|\n    +----------+---+---------------+\n    |2015-04-08|  2|     2015-04-10|\n    +----------+---+---------------+\n\n    >>> df.select('*', sf.date_add('dt', sf.lit(-1))).show()\n    +----------+---+----------------+\n    |        dt|  a|date_add(dt, -1)|\n    +----------+---+----------------+\n    |2015-04-08|  2|      2015-04-07|\n    +----------+---+----------------+\n    ",
    group: "date",
    args: [
      {
        name: "start",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "days",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long"],
        custom_input: "number",
      },
    ],
  },
  date_format: {
    doc: "\n    Converts a date/timestamp/string to a value of string in the format specified by the date\n    format given by the second argument.\n\n    A pattern could be for instance `dd.MM.yyyy` and could return a string like '18.03.1993'. All\n    pattern letters of `datetime pattern`_. can be used.\n\n    .. _datetime pattern: https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Notes\n    -----\n    Whenever possible, use specialized functions like `year`.\n\n    Parameters\n    ----------\n    date : :class:`~pyspark.sql.Column` or column name\n        input column of values to format.\n    format: literal string\n        format to use to represent datetime values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.to_date`\n    :meth:`pyspark.sql.functions.to_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp_ltz`\n    :meth:`pyspark.sql.functions.to_timestamp_ntz`\n    :meth:`pyspark.sql.functions.to_utc_timestamp`\n    :meth:`pyspark.sql.functions.try_to_timestamp`\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        string value representing formatted datetime.\n\n    Examples\n    --------\n    Example 1: Format a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.date_format('dt', 'MM/dd/yyyy')).show()\n    +----------+----------+---------------------------+\n    |        dt|typeof(dt)|date_format(dt, MM/dd/yyyy)|\n    +----------+----------+---------------------------+\n    |2015-04-08|    string|                 04/08/2015|\n    |2024-10-31|    string|                 10/31/2024|\n    +----------+----------+---------------------------+\n\n    Example 2: Format a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.date_format('ts', 'yy=MM=dd HH=mm=ss')).show()\n    +-------------------+----------+----------------------------------+\n    |                 ts|typeof(ts)|date_format(ts, yy=MM=dd HH=mm=ss)|\n    +-------------------+----------+----------------------------------+\n    |2015-04-08 13:08:15|    string|                 15=04=08 13=08=15|\n    |2024-10-31 10:09:16|    string|                 24=10=31 10=09=16|\n    +-------------------+----------+----------------------------------+\n\n    Example 3: Format a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.date_format('dt', 'yy--MM--dd')).show()\n    +----------+----------+---------------------------+\n    |        dt|typeof(dt)|date_format(dt, yy--MM--dd)|\n    +----------+----------+---------------------------+\n    |2015-04-08|      date|                 15--04--08|\n    |2024-10-31|      date|                 24--10--31|\n    +----------+----------+---------------------------+\n\n    Example 4: Format a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.date_format('ts', 'yy=MM=dd HH=mm=ss')).show()\n    +-------------------+----------+----------------------------------+\n    |                 ts|typeof(ts)|date_format(ts, yy=MM=dd HH=mm=ss)|\n    +-------------------+----------+----------------------------------+\n    |2015-04-08 13:08:15| timestamp|                 15=04=08 13=08=15|\n    |2024-10-31 10:09:16| timestamp|                 24=10=31 10=09=16|\n    +-------------------+----------+----------------------------------+\n    ",
    group: "date",
    args: [
      {
        name: "date",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "format",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  date_sub: {
    doc: "\n    Returns the date that is `days` days before `start`. If `days` is a negative value\n    then these amount of days will be added to `start`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    start : :class:`~pyspark.sql.Column` or column name\n        date column to work on.\n    days : :class:`~pyspark.sql.Column` or column name or int\n        how many days before the given date to calculate.\n        Accepts negative value as well to calculate forward in time.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        a date before/after given number of days.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.dateadd`\n    :meth:`pyspark.sql.functions.date_add`\n    :meth:`pyspark.sql.functions.datediff`\n    :meth:`pyspark.sql.functions.date_diff`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08', 2,)], 'struct<dt:string,a:int>')\n    >>> df.select('*', sf.date_sub(df.dt, 1)).show()\n    +----------+---+---------------+\n    |        dt|  a|date_sub(dt, 1)|\n    +----------+---+---------------+\n    |2015-04-08|  2|     2015-04-07|\n    +----------+---+---------------+\n\n    >>> df.select('*', sf.date_sub('dt', 'a')).show()\n    +----------+---+---------------+\n    |        dt|  a|date_sub(dt, a)|\n    +----------+---+---------------+\n    |2015-04-08|  2|     2015-04-06|\n    +----------+---+---------------+\n\n    >>> df.select('*', sf.date_sub('dt', sf.lit(-1))).show()\n    +----------+---+----------------+\n    |        dt|  a|date_sub(dt, -1)|\n    +----------+---+----------------+\n    |2015-04-08|  2|      2015-04-09|\n    +----------+---+----------------+\n    ",
    group: "date",
    args: [
      {
        name: "start",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "days",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long"],
        custom_input: "number",
      },
    ],
  },
  datediff: {
    doc: "\n    Returns the number of days from `start` to `end`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    end : :class:`~pyspark.sql.Column` or column name\n        to date column to work on.\n    start : :class:`~pyspark.sql.Column` or column name\n        from date column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        difference in days between two dates.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.dateadd`\n    :meth:`pyspark.sql.functions.date_add`\n    :meth:`pyspark.sql.functions.date_sub`\n    :meth:`pyspark.sql.functions.date_diff`\n    :meth:`pyspark.sql.functions.timestamp_diff`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08','2015-05-10')], ['d1', 'd2'])\n    >>> df.select('*', sf.datediff('d1', 'd2')).show()\n    +----------+----------+----------------+\n    |        d1|        d2|datediff(d1, d2)|\n    +----------+----------+----------------+\n    |2015-04-08|2015-05-10|             -32|\n    +----------+----------+----------------+\n\n    >>> df.select('*', sf.datediff(df.d2, df.d1)).show()\n    +----------+----------+----------------+\n    |        d1|        d2|datediff(d2, d1)|\n    +----------+----------+----------------+\n    |2015-04-08|2015-05-10|              32|\n    +----------+----------+----------------+\n    ",
    group: "date",
    args: [
      {
        name: "end",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "start",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  day: {
    doc: "\n    Extract the day of the month of a given date/timestamp as integer.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        day of the month for given date/timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.year`\n    :meth:`pyspark.sql.functions.quarter`\n    :meth:`pyspark.sql.functions.month`\n    :meth:`pyspark.sql.functions.hour`\n    :meth:`pyspark.sql.functions.minute`\n    :meth:`pyspark.sql.functions.second`\n    :meth:`pyspark.sql.functions.dayname`\n    :meth:`pyspark.sql.functions.dayofyear`\n    :meth:`pyspark.sql.functions.dayofmonth`\n    :meth:`pyspark.sql.functions.dayofweek`\n    :meth:`pyspark.sql.functions.extract`\n    :meth:`pyspark.sql.functions.datepart`\n    :meth:`pyspark.sql.functions.date_part`\n\n    Examples\n    --------\n    Example 1: Extract the day of the month from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.day('dt')).show()\n    +----------+----------+-------+\n    |        dt|typeof(dt)|day(dt)|\n    +----------+----------+-------+\n    |2015-04-08|    string|      8|\n    |2024-10-31|    string|     31|\n    +----------+----------+-------+\n\n    Example 2: Extract the day of the month from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.day('ts')).show()\n    +-------------------+----------+-------+\n    |                 ts|typeof(ts)|day(ts)|\n    +-------------------+----------+-------+\n    |2015-04-08 13:08:15|    string|      8|\n    |2024-10-31 10:09:16|    string|     31|\n    +-------------------+----------+-------+\n\n    Example 3: Extract the day of the month from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.day('dt')).show()\n    +----------+----------+-------+\n    |        dt|typeof(dt)|day(dt)|\n    +----------+----------+-------+\n    |2015-04-08|      date|      8|\n    |2024-10-31|      date|     31|\n    +----------+----------+-------+\n\n    Example 4: Extract the day of the month from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.day('ts')).show()\n    +-------------------+----------+-------+\n    |                 ts|typeof(ts)|day(ts)|\n    +-------------------+----------+-------+\n    |2015-04-08 13:08:15| timestamp|      8|\n    |2024-10-31 10:09:16| timestamp|     31|\n    +-------------------+----------+-------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  dayofmonth: {
    doc: "\n    Extract the day of the month of a given date/timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.dayofyear`\n    :meth:`pyspark.sql.functions.dayofweek`\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        day of the month for given date/timestamp as integer.\n\n    Examples\n    --------\n    Example 1: Extract the day of the month from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofmonth('dt')).show()\n    +----------+----------+--------------+\n    |        dt|typeof(dt)|dayofmonth(dt)|\n    +----------+----------+--------------+\n    |2015-04-08|    string|             8|\n    |2024-10-31|    string|            31|\n    +----------+----------+--------------+\n\n    Example 2: Extract the day of the month from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofmonth('ts')).show()\n    +-------------------+----------+--------------+\n    |                 ts|typeof(ts)|dayofmonth(ts)|\n    +-------------------+----------+--------------+\n    |2015-04-08 13:08:15|    string|             8|\n    |2024-10-31 10:09:16|    string|            31|\n    +-------------------+----------+--------------+\n\n    Example 3: Extract the day of the month from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofmonth('dt')).show()\n    +----------+----------+--------------+\n    |        dt|typeof(dt)|dayofmonth(dt)|\n    +----------+----------+--------------+\n    |2015-04-08|      date|             8|\n    |2024-10-31|      date|            31|\n    +----------+----------+--------------+\n\n    Example 4: Extract the day of the month from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofmonth('ts')).show()\n    +-------------------+----------+--------------+\n    |                 ts|typeof(ts)|dayofmonth(ts)|\n    +-------------------+----------+--------------+\n    |2015-04-08 13:08:15| timestamp|             8|\n    |2024-10-31 10:09:16| timestamp|            31|\n    +-------------------+----------+--------------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  dayofweek: {
    doc: "\n    Extract the day of the week of a given date/timestamp as integer.\n    Ranges from 1 for a Sunday through to 7 for a Saturday\n\n    .. versionadded:: 2.3.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        day of the week for given date/timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.dayofyear`\n    :meth:`pyspark.sql.functions.dayofmonth`\n\n    Examples\n    --------\n    Example 1: Extract the day of the week from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofweek('dt')).show()\n    +----------+----------+-------------+\n    |        dt|typeof(dt)|dayofweek(dt)|\n    +----------+----------+-------------+\n    |2015-04-08|    string|            4|\n    |2024-10-31|    string|            5|\n    +----------+----------+-------------+\n\n    Example 2: Extract the day of the week from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofweek('ts')).show()\n    +-------------------+----------+-------------+\n    |                 ts|typeof(ts)|dayofweek(ts)|\n    +-------------------+----------+-------------+\n    |2015-04-08 13:08:15|    string|            4|\n    |2024-10-31 10:09:16|    string|            5|\n    +-------------------+----------+-------------+\n\n    Example 3: Extract the day of the week from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofweek('dt')).show()\n    +----------+----------+-------------+\n    |        dt|typeof(dt)|dayofweek(dt)|\n    +----------+----------+-------------+\n    |2015-04-08|      date|            4|\n    |2024-10-31|      date|            5|\n    +----------+----------+-------------+\n\n    Example 4: Extract the day of the week from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofweek('ts')).show()\n    +-------------------+----------+-------------+\n    |                 ts|typeof(ts)|dayofweek(ts)|\n    +-------------------+----------+-------------+\n    |2015-04-08 13:08:15| timestamp|            4|\n    |2024-10-31 10:09:16| timestamp|            5|\n    +-------------------+----------+-------------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  dayofyear: {
    doc: "\n    Extract the day of the year of a given date/timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        day of the year for given date/timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.dayofyear`\n    :meth:`pyspark.sql.functions.dayofmonth`\n\n    Examples\n    --------\n    Example 1: Extract the day of the year from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofyear('dt')).show()\n    +----------+----------+-------------+\n    |        dt|typeof(dt)|dayofyear(dt)|\n    +----------+----------+-------------+\n    |2015-04-08|    string|           98|\n    |2024-10-31|    string|          305|\n    +----------+----------+-------------+\n\n    Example 2: Extract the day of the year from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofyear('ts')).show()\n    +-------------------+----------+-------------+\n    |                 ts|typeof(ts)|dayofyear(ts)|\n    +-------------------+----------+-------------+\n    |2015-04-08 13:08:15|    string|           98|\n    |2024-10-31 10:09:16|    string|          305|\n    +-------------------+----------+-------------+\n\n    Example 3: Extract the day of the year from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.dayofyear('dt')).show()\n    +----------+----------+-------------+\n    |        dt|typeof(dt)|dayofyear(dt)|\n    +----------+----------+-------------+\n    |2015-04-08|      date|           98|\n    |2024-10-31|      date|          305|\n    +----------+----------+-------------+\n\n    Example 4: Extract the day of the year from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.dayofyear('ts')).show()\n    +-------------------+----------+-------------+\n    |                 ts|typeof(ts)|dayofyear(ts)|\n    +-------------------+----------+-------------+\n    |2015-04-08 13:08:15| timestamp|           98|\n    |2024-10-31 10:09:16| timestamp|          305|\n    +-------------------+----------+-------------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  endswith: {
    doc: '\n    Returns a boolean. The value is True if str ends with suffix.\n    Returns NULL if either input expression is NULL. Otherwise, returns False.\n    Both str or suffix must be of STRING or BINARY type.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or str\n        A column of string.\n    suffix : :class:`~pyspark.sql.Column` or str\n        A column of string, the suffix.\n\n    Examples\n    --------\n    >>> df = spark.createDataFrame([("Spark SQL", "Spark",)], ["a", "b"])\n    >>> df.select(endswith(df.a, df.b).alias(\'r\')).collect()\n    [Row(r=False)]\n\n    >>> df = spark.createDataFrame([("414243", "4243",)], ["e", "f"])\n    >>> df = df.select(to_binary("e").alias("e"), to_binary("f").alias("f"))\n    >>> df.printSchema()\n    root\n     |-- e: binary (nullable = true)\n     |-- f: binary (nullable = true)\n    >>> df.select(endswith("e", "f"), endswith("f", "e")).show()\n    +--------------+--------------+\n    |endswith(e, f)|endswith(f, e)|\n    +--------------+--------------+\n    |          true|         false|\n    +--------------+--------------+\n    ',
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "suffix",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  exp: {
    doc: '\n    Computes the exponential of the given value.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        column to calculate exponential for.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        exponential of the given value.\n\n    Examples\n    --------\n    Example 1: Compute the exponential\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.sql("SELECT id AS value FROM RANGE(5)")\n    >>> df.select("*", sf.exp(df.value)).show()\n    +-----+------------------+\n    |value|        EXP(value)|\n    +-----+------------------+\n    |    0|               1.0|\n    |    1|2.7182818284590...|\n    |    2|  7.38905609893...|\n    |    3|20.085536923187...|\n    |    4|54.598150033144...|\n    +-----+------------------+\n\n    Example 2: Compute the exponential of invalid values\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (FLOAT(\'NAN\')), (NULL) AS TAB(value)"\n    ... ).select("*", sf.exp("value")).show()\n    +-----+----------+\n    |value|EXP(value)|\n    +-----+----------+\n    |  NaN|       NaN|\n    | NULL|      NULL|\n    +-----+----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  factorial: {
    doc: "\n    Computes the factorial of the given value.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        a column to calculate factorial for.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        factorial of given value.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(10).select(\"*\", sf.factorial('id')).show()\n    +---+-------------+\n    | id|factorial(id)|\n    +---+-------------+\n    |  0|            1|\n    |  1|            1|\n    |  2|            2|\n    |  3|            6|\n    |  4|           24|\n    |  5|          120|\n    |  6|          720|\n    |  7|         5040|\n    |  8|        40320|\n    |  9|       362880|\n    +---+-------------+\n    ",
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  flatten: {
    doc: "\n    Array function: creates a single array from an array of arrays.\n    If a structure of nested arrays is deeper than two levels,\n    only one level of nesting is removed.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The name of the column or expression to be flattened.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that contains the flattened array.\n\n    Examples\n    --------\n    Example 1: Flattening a simple nested array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([[1, 2, 3], [4, 5], [6]],)], ['data'])\n    >>> df.select(sf.flatten(df.data)).show()\n    +------------------+\n    |     flatten(data)|\n    +------------------+\n    |[1, 2, 3, 4, 5, 6]|\n    +------------------+\n\n    Example 2: Flattening an array with null values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([None, [4, 5]],)], ['data'])\n    >>> df.select(sf.flatten(df.data)).show()\n    +-------------+\n    |flatten(data)|\n    +-------------+\n    |         NULL|\n    +-------------+\n\n    Example 3: Flattening an array with more than two levels of nesting\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([[[1, 2], [3, 4]], [[5, 6], [7, 8]]],)], ['data'])\n    >>> df.select(sf.flatten(df.data)).show(truncate=False)\n    +--------------------------------+\n    |flatten(data)                   |\n    +--------------------------------+\n    |[[1, 2], [3, 4], [5, 6], [7, 8]]|\n    +--------------------------------+\n\n    Example 4: Flattening an array with mixed types\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([['a', 'b', 'c'], [1, 2, 3]],)], ['data'])\n    >>> df.select(sf.flatten(df.data)).show()\n    +------------------+\n    |     flatten(data)|\n    +------------------+\n    |[a, b, c, 1, 2, 3]|\n    +------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  floor: {
    doc: "\n    Computes the floor of the given value.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        The target column or column name to compute the floor on.\n    scale : :class:`~pyspark.sql.Column` or int, optional\n        An optional parameter to control the rounding behavior.\n\n        .. versionadded:: 4.0.0\n\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        nearest integer that is less than or equal to given value.\n\n    Examples\n    --------\n    Example 1: Compute the floor of a column value\n\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.floor(sf.lit(2.5))).show()\n    +----------+\n    |FLOOR(2.5)|\n    +----------+\n    |         2|\n    +----------+\n\n    Example 2: Compute the floor of a column value with a specified scale\n\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.floor(sf.lit(2.1267), sf.lit(2))).show()\n    +----------------+\n    |floor(2.1267, 2)|\n    +----------------+\n    |            2.12|\n    +----------------+\n    ",
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "scale",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  from_utc_timestamp: {
    doc: "\n    This is a common function for databases supporting TIMESTAMP WITHOUT TIMEZONE. This function\n    takes a timestamp which is timezone-agnostic, and interprets it as a timestamp in UTC, and\n    renders that timestamp as a timestamp in the given time zone.\n\n    However, timestamp in Spark represents number of microseconds from the Unix epoch, which is not\n    timezone-agnostic. So in Spark this function just shift the timestamp value from UTC timezone to\n    the given timezone.\n\n    This function may return confusing result if the input is a string with timezone, e.g.\n    '2018-03-13T06:18:23+00:00'. The reason is that, Spark firstly cast the string to timestamp\n    according to the timezone in the string, and finally display the result by converting the\n    timestamp to string according to the session local timezone.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    timestamp : :class:`~pyspark.sql.Column` or column name\n        the column that contains timestamps\n    tz : :class:`~pyspark.sql.Column` or literal string\n        A string detailing the time zone ID that the input should be adjusted to. It should\n        be in the format of either region-based zone IDs or zone offsets. Region IDs must\n        have the form 'area/city', such as 'America/Los_Angeles'. Zone offsets must be in\n        the format '(+|-)HH:mm', for example '-08:00' or '+01:00'. Also 'UTC' and 'Z' are\n        supported as aliases of '+00:00'. Other short names are not recommended to use\n        because they can be ambiguous.\n\n        .. versionchanged:: 2.4\n           `tz` can take a :class:`~pyspark.sql.Column` containing timezone ID strings.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        timestamp value represented in given timezone.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.to_utc_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp_ltz`\n    :meth:`pyspark.sql.functions.to_timestamp_ntz`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('1997-02-28 10:30:00', 'JST')], ['ts', 'tz'])\n    >>> df.select('*', sf.from_utc_timestamp('ts', 'PST')).show()\n    +-------------------+---+---------------------------+\n    |                 ts| tz|from_utc_timestamp(ts, PST)|\n    +-------------------+---+---------------------------+\n    |1997-02-28 10:30:00|JST|        1997-02-28 02:30:00|\n    +-------------------+---+---------------------------+\n\n    >>> df.select('*', sf.from_utc_timestamp(df.ts, df.tz)).show()\n    +-------------------+---+--------------------------+\n    |                 ts| tz|from_utc_timestamp(ts, tz)|\n    +-------------------+---+--------------------------+\n    |1997-02-28 10:30:00|JST|       1997-02-28 19:30:00|\n    +-------------------+---+--------------------------+\n    ",
    group: "date",
    args: [
      {
        name: "timestamp",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "tz",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  get: {
    doc: '\n    Array function: Returns the element of an array at the given (0-based) index.\n    If the index points outside of the array boundaries, then this function\n    returns NULL.\n\n    .. versionadded:: 3.4.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        Name of the column containing the array.\n    index : :class:`~pyspark.sql.Column` or str or int\n        Index to check for in the array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        Value at the given position.\n\n    Notes\n    -----\n    The position is not 1-based, but 0-based index.\n    Supports Spark Connect.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.element_at`\n\n    Examples\n    --------\n    Example 1: Getting an element at a fixed position\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"],)], [\'data\'])\n    >>> df.select(sf.get(df.data, 1)).show()\n    +------------+\n    |get(data, 1)|\n    +------------+\n    |           b|\n    +------------+\n\n    Example 2: Getting an element at a position outside the array boundaries\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"],)], [\'data\'])\n    >>> df.select(sf.get(df.data, 3)).show()\n    +------------+\n    |get(data, 3)|\n    +------------+\n    |        NULL|\n    +------------+\n\n    Example 3: Getting an element at a position specified by another column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"], 2)], [\'data\', \'index\'])\n    >>> df.select(sf.get(df.data, df.index)).show()\n    +----------------+\n    |get(data, index)|\n    +----------------+\n    |               c|\n    +----------------+\n\n\n    Example 4: Getting an element at a position calculated from another column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"], 2)], [\'data\', \'index\'])\n    >>> df.select(sf.get(df.data, df.index - 1)).show()\n    +----------------------+\n    |get(data, (index - 1))|\n    +----------------------+\n    |                     b|\n    +----------------------+\n\n    Example 5: Getting an element at a negative position\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(["a", "b", "c"], )], [\'data\'])\n    >>> df.select(sf.get(df.data, -1)).show()\n    +-------------+\n    |get(data, -1)|\n    +-------------+\n    |         NULL|\n    +-------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "index",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  greatest: {
    doc: "\n    Returns the greatest value of the list of column names, skipping null values.\n    This function takes at least 2 parameters. It will return null if all parameters are null.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols: :class:`~pyspark.sql.Column` or column name\n        columns to check for greatest value.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        greatest value.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.least`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([(1, 4, 3)], ['a', 'b', 'c'])\n    >>> df.select(\"*\", sf.greatest(df.a, \"b\", df.c)).show()\n    +---+---+---+-----------------+\n    |  a|  b|  c|greatest(a, b, c)|\n    +---+---+---+-----------------+\n    |  1|  4|  3|                4|\n    +---+---+---+-----------------+\n    ",
    group: "misc",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  hash: {
    doc: "Calculates the hash code of given columns, and returns the result as an int column.\n\n    .. versionadded:: 2.0.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols : :class:`~pyspark.sql.Column` or column name\n        one or more columns to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        hash value as int column.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.xxhash64`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('ABC', 'DEF')], ['c1', 'c2'])\n    >>> df.select('*', sf.hash('c1')).show()\n    +---+---+----------+\n    | c1| c2|  hash(c1)|\n    +---+---+----------+\n    |ABC|DEF|-757602832|\n    +---+---+----------+\n\n    >>> df.select('*', sf.hash('c1', df.c2)).show()\n    +---+---+------------+\n    | c1| c2|hash(c1, c2)|\n    +---+---+------------+\n    |ABC|DEF|   599895104|\n    +---+---+------------+\n\n    >>> df.select('*', sf.hash('*')).show()\n    +---+---+------------+\n    | c1| c2|hash(c1, c2)|\n    +---+---+------------+\n    |ABC|DEF|   599895104|\n    +---+---+------------+\n    ",
    group: "misc",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  hour: {
    doc: "\n    Extract the hours of a given timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        hour part of the timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.year`\n    :meth:`pyspark.sql.functions.quarter`\n    :meth:`pyspark.sql.functions.month`\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.minute`\n    :meth:`pyspark.sql.functions.second`\n    :meth:`pyspark.sql.functions.extract`\n    :meth:`pyspark.sql.functions.datepart`\n    :meth:`pyspark.sql.functions.date_part`\n\n    Examples\n    --------\n    Example 1: Extract the hours from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.hour('ts')).show()\n    +-------------------+----------+--------+\n    |                 ts|typeof(ts)|hour(ts)|\n    +-------------------+----------+--------+\n    |2015-04-08 13:08:15|    string|      13|\n    |2024-10-31 10:09:16|    string|      10|\n    +-------------------+----------+--------+\n\n    Example 2: Extract the hours from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.hour('ts')).show()\n    +-------------------+----------+--------+\n    |                 ts|typeof(ts)|hour(ts)|\n    +-------------------+----------+--------+\n    |2015-04-08 13:08:15| timestamp|      13|\n    |2024-10-31 10:09:16| timestamp|      10|\n    +-------------------+----------+--------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  is_valid_utf8: {
    doc: '\n    Returns true if the input is a valid UTF-8 string, otherwise returns false.\n\n    .. versionadded:: 4.0.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        A column of strings, each representing a UTF-8 byte sequence.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        whether the input string is a valid UTF-8 string.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.make_valid_utf8`\n    :meth:`pyspark.sql.functions.validate_utf8`\n    :meth:`pyspark.sql.functions.try_validate_utf8`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.is_valid_utf8(sf.lit("SparkSQL"))).show()\n    +-----------------------+\n    |is_valid_utf8(SparkSQL)|\n    +-----------------------+\n    |                   true|\n    +-----------------------+\n    ',
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  isnan: {
    doc: 'An expression that returns true if the column is NaN.\n\n    .. versionadded:: 1.6.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        True if value is NaN and False otherwise.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(1.0, float(\'nan\')), (float(\'nan\'), 2.0)], ("a", "b"))\n    >>> df.select("*", sf.isnan("a"), sf.isnan(df.b)).show()\n    +---+---+--------+--------+\n    |  a|  b|isnan(a)|isnan(b)|\n    +---+---+--------+--------+\n    |1.0|NaN|   false|    true|\n    |NaN|2.0|    true|   false|\n    +---+---+--------+--------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  isnull: {
    doc: 'An expression that returns true if the column is null.\n\n    .. versionadded:: 1.6.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        True if value is null and False otherwise.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(1, None), (None, 2)], ("a", "b"))\n    >>> df.select("*", sf.isnull("a"), isnull(df.b)).show()\n    +----+----+-----------+-----------+\n    |   a|   b|(a IS NULL)|(b IS NULL)|\n    +----+----+-----------+-----------+\n    |   1|NULL|      false|       true|\n    |NULL|   2|       true|      false|\n    +----+----+-----------+-----------+\n    ',
    group: "misc",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  last_day: {
    doc: "\n    Returns the last day of the month which the given date belongs to.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    date : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        last day of the month.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('1997-02-10',)], ['dt'])\n    >>> df.select('*', sf.last_day(df.dt)).show()\n    +----------+------------+\n    |        dt|last_day(dt)|\n    +----------+------------+\n    |1997-02-10|  1997-02-28|\n    +----------+------------+\n\n    >>> df.select('*', sf.last_day('dt')).show()\n    +----------+------------+\n    |        dt|last_day(dt)|\n    +----------+------------+\n    |1997-02-10|  1997-02-28|\n    +----------+------------+\n    ",
    group: "date",
    args: [
      {
        name: "date",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  least: {
    doc: "\n    Returns the least value of the list of column names, skipping null values.\n    This function takes at least 2 parameters. It will return null if all parameters are null.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    cols : :class:`~pyspark.sql.Column` or column name\n        column names or columns to be compared\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        least value.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.greatest`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([(1, 4, 3)], ['a', 'b', 'c'])\n    >>> df.select(\"*\", sf.least(df.a, \"b\", df.c)).show()\n    +---+---+---+--------------+\n    |  a|  b|  c|least(a, b, c)|\n    +---+---+---+--------------+\n    |  1|  4|  3|             1|\n    +---+---+---+--------------+\n    ",
    group: "misc",
    args: [
      {
        name: "cols",
        selector: "multi",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  length: {
    doc: "Computes the character length of string data or number of bytes of binary data.\n    The length of character data includes the trailing spaces. The length of binary data\n    includes binary zeros.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        target column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        length of the value.\n\n    Examples\n    --------\n    >>> spark.createDataFrame([('ABC ',)], ['a']).select(length('a').alias('length')).collect()\n    [Row(length=4)]\n    ",
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  levenshtein: {
    doc: "Computes the Levenshtein distance of the two given strings.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    left : :class:`~pyspark.sql.Column` or column name\n        first column value.\n    right : :class:`~pyspark.sql.Column` or column name\n        second column value.\n    threshold : int, optional\n        if set when the levenshtein distance of the two given strings\n        less than or equal to a given threshold then return result distance, or -1\n\n        .. versionadded: 3.5.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        Levenshtein distance as integer value.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('kitten', 'sitting',)], ['l', 'r'])\n    >>> df.select('*', sf.levenshtein('l', 'r')).show()\n    +------+-------+-----------------+\n    |     l|      r|levenshtein(l, r)|\n    +------+-------+-----------------+\n    |kitten|sitting|                3|\n    +------+-------+-----------------+\n\n    >>> df.select('*', sf.levenshtein(df.l, df.r, 2)).show()\n    +------+-------+--------------------+\n    |     l|      r|levenshtein(l, r, 2)|\n    +------+-------+--------------------+\n    |kitten|sitting|                  -1|\n    +------+-------+--------------------+\n    ",
    group: "string",
    args: [
      {
        name: "left",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "right",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "threshold",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  ln: {
    doc: "Returns the natural logarithm of the argument.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        a column to calculate logariphm for.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        natural logarithm of given value.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(10).select(\"*\", sf.ln('id')).show()\n    +---+------------------+\n    | id|            ln(id)|\n    +---+------------------+\n    |  0|              NULL|\n    |  1|               0.0|\n    |  2|0.6931471805599...|\n    |  3|1.0986122886681...|\n    |  4|1.3862943611198...|\n    |  5|1.6094379124341...|\n    |  6| 1.791759469228...|\n    |  7|1.9459101490553...|\n    |  8|2.0794415416798...|\n    |  9|2.1972245773362...|\n    +---+------------------+\n    ",
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  log: {
    doc: 'Returns the first argument-based logarithm of the second argument.\n\n    If there is only one argument, then this takes the natural logarithm of the argument.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    arg1 : :class:`~pyspark.sql.Column`, str or float\n        base number or actual number (in this case base is `e`)\n    arg2 : :class:`~pyspark.sql.Column`, str or float, optional\n        number to calculate logariphm for.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        logariphm of given value.\n\n    Examples\n    --------\n    Example 1: Specify both base number and the input value\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.sql("SELECT * FROM VALUES (1), (2), (4) AS t(value)")\n    >>> df.select("*", sf.log(2.0, df.value)).show()\n    +-----+---------------+\n    |value|LOG(2.0, value)|\n    +-----+---------------+\n    |    1|            0.0|\n    |    2|            1.0|\n    |    4|            2.0|\n    +-----+---------------+\n\n    Example 2: Return NULL for invalid input values\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.sql("SELECT * FROM VALUES (1), (2), (0), (-1), (NULL) AS t(value)")\n    >>> df.select("*", sf.log(3.0, df.value)).show()\n    +-----+------------------+\n    |value|   LOG(3.0, value)|\n    +-----+------------------+\n    |    1|               0.0|\n    |    2|0.6309297535714...|\n    |    0|              NULL|\n    |   -1|              NULL|\n    | NULL|              NULL|\n    +-----+------------------+\n\n    Example 3: Specify only the input value (Natural logarithm)\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.sql("SELECT * FROM VALUES (1), (2), (4) AS t(value)")\n    >>> df.select("*", sf.log(df.value)).show()\n    +-----+------------------+\n    |value|         ln(value)|\n    +-----+------------------+\n    |    1|               0.0|\n    |    2|0.6931471805599...|\n    |    4|1.3862943611198...|\n    +-----+------------------+\n    ',
    group: "math",
    args: [
      {
        name: "arg1",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "arg2",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  lower: {
    doc: '\n    Converts a string expression to lower case.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        lower case values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.upper`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["Spark", "PySpark", "Pandas API"], "STRING")\n    >>> df.select("*", sf.lower("value")).show()\n    +----------+------------+\n    |     value|lower(value)|\n    +----------+------------+\n    |     Spark|       spark|\n    |   PySpark|     pyspark|\n    |Pandas API|  pandas api|\n    +----------+------------+\n    ',
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  lpad: {
    doc: "\n    Left-pad the string column to width `len` with `pad`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    len : :class:`~pyspark.sql.Column` or int\n        length of the final string.\n\n        .. versionchanged:: 4.0.0\n             `pattern` now accepts column.\n\n    pad : :class:`~pyspark.sql.Column` or literal string\n        chars to prepend.\n\n        .. versionchanged:: 4.0.0\n             `pattern` now accepts column.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        left padded result.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.rpad`\n\n    Examples\n    --------\n    Example 1: Pad with a literal string\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('abcd',), ('xyz',), ('12',)], ['s',])\n    >>> df.select(\"*\", sf.lpad(df.s, 6, '#')).show()\n    +----+-------------+\n    |   s|lpad(s, 6, #)|\n    +----+-------------+\n    |abcd|       ##abcd|\n    | xyz|       ###xyz|\n    |  12|       ####12|\n    +----+-------------+\n\n    Example 2: Pad with a bytes column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('abcd',), ('xyz',), ('12',)], ['s',])\n    >>> df.select(\"*\", sf.lpad(df.s, 6, sf.lit(b\"uv\"))).show()\n    +----+-------------------+\n    |   s|lpad(s, 6, X'7576')|\n    +----+-------------------+\n    |abcd|             uvabcd|\n    | xyz|             uvuxyz|\n    |  12|             uvuv12|\n    +----+-------------------+\n    ",
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "len",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
      {
        name: "pad",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  ltrim: {
    doc: '\n    Trim the spaces from left end for the specified string value.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    trim : :class:`~pyspark.sql.Column` or column name, optional\n        The trim string characters to trim, the default value is a single space\n\n        .. versionadded:: 4.0.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        left trimmed values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.trim`\n    :meth:`pyspark.sql.functions.rtrim`\n\n    Examples\n    --------\n    Example 1: Trim the spaces\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["   Spark", "Spark  ", " Spark"], "STRING")\n    >>> df.select("*", sf.ltrim("value")).show()\n    +--------+------------+\n    |   value|ltrim(value)|\n    +--------+------------+\n    |   Spark|       Spark|\n    | Spark  |     Spark  |\n    |   Spark|       Spark|\n    +--------+------------+\n\n    Example 2: Trim specified characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["***Spark", "Spark**", "*Spark"], "STRING")\n    >>> df.select("*", sf.ltrim("value", sf.lit("*"))).show()\n    +--------+--------------------------+\n    |   value|TRIM(LEADING * FROM value)|\n    +--------+--------------------------+\n    |***Spark|                     Spark|\n    | Spark**|                   Spark**|\n    |  *Spark|                     Spark|\n    +--------+--------------------------+\n\n    Example 3: Trim a column containing different characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("**Spark*", "*"), ("==Spark=", "=")], ["value", "t"])\n    >>> df.select("*", sf.ltrim("value", "t")).show()\n    +--------+---+--------------------------+\n    |   value|  t|TRIM(LEADING t FROM value)|\n    +--------+---+--------------------------+\n    |**Spark*|  *|                    Spark*|\n    |==Spark=|  =|                    Spark=|\n    +--------+---+--------------------------+\n    ',
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "trim",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  make_valid_utf8: {
    doc: '\n    Returns a new string in which all invalid UTF-8 byte sequences, if any, are replaced by the\n    Unicode replacement character (U+FFFD).\n\n    .. versionadded:: 4.0.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        A column of strings, each representing a UTF-8 byte sequence.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the valid UTF-8 version of the given input string.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.is_valid_utf8`\n    :meth:`pyspark.sql.functions.validate_utf8`\n    :meth:`pyspark.sql.functions.try_validate_utf8`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.make_valid_utf8(sf.lit("SparkSQL"))).show()\n    +-------------------------+\n    |make_valid_utf8(SparkSQL)|\n    +-------------------------+\n    |                 SparkSQL|\n    +-------------------------+\n    ',
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  md5: {
    doc: "Calculates the MD5 digest and returns the value as a 32 character hex string.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the column for computed results.\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('ABC',)], ['a'])\n    >>> df.select('*', sf.md5('a')).show(truncate=False)\n    +---+--------------------------------+\n    |a  |md5(a)                          |\n    +---+--------------------------------+\n    |ABC|902fbdd2b1df0c4f70b4a5d23525e932|\n    +---+--------------------------------+\n    ",
    group: "misc",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  minute: {
    doc: "\n    Extract the minutes of a given timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.year`\n    :meth:`pyspark.sql.functions.quarter`\n    :meth:`pyspark.sql.functions.month`\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.hour`\n    :meth:`pyspark.sql.functions.second`\n    :meth:`pyspark.sql.functions.extract`\n    :meth:`pyspark.sql.functions.datepart`\n    :meth:`pyspark.sql.functions.date_part`\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        minutes part of the timestamp as integer.\n\n    Examples\n    --------\n    Example 1: Extract the minutes from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.minute('ts')).show()\n    +-------------------+----------+----------+\n    |                 ts|typeof(ts)|minute(ts)|\n    +-------------------+----------+----------+\n    |2015-04-08 13:08:15|    string|         8|\n    |2024-10-31 10:09:16|    string|         9|\n    +-------------------+----------+----------+\n\n    Example 2: Extract the minutes from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.minute('ts')).show()\n    +-------------------+----------+----------+\n    |                 ts|typeof(ts)|minute(ts)|\n    +-------------------+----------+----------+\n    |2015-04-08 13:08:15| timestamp|         8|\n    |2024-10-31 10:09:16| timestamp|         9|\n    +-------------------+----------+----------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  month: {
    doc: "\n    Extract the month of a given date/timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        month part of the date/timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.year`\n    :meth:`pyspark.sql.functions.quarter`\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.hour`\n    :meth:`pyspark.sql.functions.minute`\n    :meth:`pyspark.sql.functions.second`\n    :meth:`pyspark.sql.functions.monthname`\n    :meth:`pyspark.sql.functions.extract`\n    :meth:`pyspark.sql.functions.datepart`\n    :meth:`pyspark.sql.functions.date_part`\n\n    Examples\n    --------\n    Example 1: Extract the month from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.month('dt')).show()\n    +----------+----------+---------+\n    |        dt|typeof(dt)|month(dt)|\n    +----------+----------+---------+\n    |2015-04-08|    string|        4|\n    |2024-10-31|    string|       10|\n    +----------+----------+---------+\n\n    Example 2: Extract the month from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.month('ts')).show()\n    +-------------------+----------+---------+\n    |                 ts|typeof(ts)|month(ts)|\n    +-------------------+----------+---------+\n    |2015-04-08 13:08:15|    string|        4|\n    |2024-10-31 10:09:16|    string|       10|\n    +-------------------+----------+---------+\n\n    Example 3: Extract the month from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.month('dt')).show()\n    +----------+----------+---------+\n    |        dt|typeof(dt)|month(dt)|\n    +----------+----------+---------+\n    |2015-04-08|      date|        4|\n    |2024-10-31|      date|       10|\n    +----------+----------+---------+\n\n    Example 3: Extract the month from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.month('ts')).show()\n    +-------------------+----------+---------+\n    |                 ts|typeof(ts)|month(ts)|\n    +-------------------+----------+---------+\n    |2015-04-08 13:08:15| timestamp|        4|\n    |2024-10-31 10:09:16| timestamp|       10|\n    +-------------------+----------+---------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  months_between: {
    doc: "\n    Returns number of months between dates date1 and date2.\n    If date1 is later than date2, then the result is positive.\n    A whole number is returned if both inputs have the same day of month or both are the last day\n    of their respective months. Otherwise, the difference is calculated assuming 31 days per month.\n    The result is rounded off to 8 digits unless `roundOff` is set to `False`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    date1 : :class:`~pyspark.sql.Column` or column name\n        first date column.\n    date2 : :class:`~pyspark.sql.Column` or column name\n        second date column.\n    roundOff : bool, optional\n        whether to round (to 8 digits) the final value or not (default: True).\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        number of months between two dates.\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('1997-02-28 10:30:00', '1996-10-30')], ['d1', 'd2'])\n    >>> df.select('*', sf.months_between(df.d1, df.d2)).show()\n    +-------------------+----------+----------------------------+\n    |                 d1|        d2|months_between(d1, d2, true)|\n    +-------------------+----------+----------------------------+\n    |1997-02-28 10:30:00|1996-10-30|                  3.94959677|\n    +-------------------+----------+----------------------------+\n\n    >>> df.select('*', sf.months_between('d2', 'd1')).show()\n    +-------------------+----------+----------------------------+\n    |                 d1|        d2|months_between(d2, d1, true)|\n    +-------------------+----------+----------------------------+\n    |1997-02-28 10:30:00|1996-10-30|                 -3.94959677|\n    +-------------------+----------+----------------------------+\n\n    >>> df.select('*', sf.months_between('d1', df.d2, False)).show()\n    +-------------------+----------+-----------------------------+\n    |                 d1|        d2|months_between(d1, d2, false)|\n    +-------------------+----------+-----------------------------+\n    |1997-02-28 10:30:00|1996-10-30|           3.9495967741935...|\n    +-------------------+----------+-----------------------------+\n    ",
    group: "date",
    args: [
      {
        name: "date1",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "date2",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "roundOff",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "checkbox",
      },
    ],
  },
  pow: {
    doc: '\n    Returns the value of the first argument raised to the power of the second argument.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col1 : :class:`~pyspark.sql.Column`, column name or float\n        the base number.\n    col2 : :class:`~pyspark.sql.Column`, column name or float\n        the exponent number.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the base rased to the power the argument.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(5).select("*", sf.pow("id", 2)).show()\n    +---+------------+\n    | id|POWER(id, 2)|\n    +---+------------+\n    |  0|         0.0|\n    |  1|         1.0|\n    |  2|         4.0|\n    |  3|         9.0|\n    |  4|        16.0|\n    +---+------------+\n    ',
    group: "math",
    args: [
      {
        name: "col1",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "col2",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  rand: {
    doc: 'Generates a random column with independent and identically distributed (i.i.d.) samples\n    uniformly distributed in [0.0, 1.0).\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Notes\n    -----\n    The function is non-deterministic in general case.\n\n    Parameters\n    ----------\n    seed : int, optional\n        Seed value for the random generator.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A column of random values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.randn`\n    :meth:`pyspark.sql.functions.randstr`\n    :meth:`pyspark.sql.functions.uniform`\n\n    Examples\n    --------\n    Example 1: Generate a random column without a seed\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.range(0, 2, 1, 1).select("*", sf.rand()).show() # doctest: +SKIP\n    +---+-------------------------+\n    | id|rand(-158884697681280011)|\n    +---+-------------------------+\n    |  0|       0.9253464547887...|\n    |  1|       0.6533254118758...|\n    +---+-------------------------+\n\n    Example 2: Generate a random column with a specific seed\n\n    >>> spark.range(0, 2, 1, 1).select("*", sf.rand(seed=42)).show()\n    +---+------------------+\n    | id|          rand(42)|\n    +---+------------------+\n    |  0| 0.619189370225...|\n    |  1|0.5096018842446...|\n    +---+------------------+\n    ',
    group: "math",
    args: [
      {
        name: "seed",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  regexp_count: {
    doc: "Returns a count of the number of times that the Java regex pattern `regexp` is matched\n    in the string `str`.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    regexp : :class:`~pyspark.sql.Column` or column name\n        regex pattern to apply.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the number of times that a Java regex pattern is matched in the string.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(\"1a 2b 14m\", r\"\\d+\")], [\"str\", \"regexp\"])\n    >>> df.select('*', sf.regexp_count('str', sf.lit(r'\\d+'))).show()\n    +---------+------+----------------------+\n    |      str|regexp|regexp_count(str, \\d+)|\n    +---------+------+----------------------+\n    |1a 2b 14m|   \\d+|                     3|\n    +---------+------+----------------------+\n\n    >>> df.select('*', sf.regexp_count('str', sf.lit(r'mmm'))).show()\n    +---------+------+----------------------+\n    |      str|regexp|regexp_count(str, mmm)|\n    +---------+------+----------------------+\n    |1a 2b 14m|   \\d+|                     0|\n    +---------+------+----------------------+\n\n    >>> df.select('*', sf.regexp_count(\"str\", sf.col(\"regexp\"))).show()\n    +---------+------+-------------------------+\n    |      str|regexp|regexp_count(str, regexp)|\n    +---------+------+-------------------------+\n    |1a 2b 14m|   \\d+|                        3|\n    +---------+------+-------------------------+\n\n    >>> df.select('*', sf.regexp_count(sf.col('str'), \"regexp\")).show()\n    +---------+------+-------------------------+\n    |      str|regexp|regexp_count(str, regexp)|\n    +---------+------+-------------------------+\n    |1a 2b 14m|   \\d+|                        3|\n    +---------+------+-------------------------+\n    ",
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "regexp",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  regexp_extract: {
    doc: "Extract a specific group matched by the Java regex `regexp`, from the specified string column.\n    If the regex did not match, or the specified group did not match, an empty string is returned.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    pattern : str\n        regex pattern to apply.\n    idx : int\n        matched group id.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        matched value specified by `idx` group id.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.regexp_extract_all`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('100-200',)], ['str'])\n    >>> df.select('*', sf.regexp_extract('str', r'(\\d+)-(\\d+)', 1)).show()\n    +-------+-----------------------------------+\n    |    str|regexp_extract(str, (\\d+)-(\\d+), 1)|\n    +-------+-----------------------------------+\n    |100-200|                                100|\n    +-------+-----------------------------------+\n\n    >>> df = spark.createDataFrame([('foo',)], ['str'])\n    >>> df.select('*', sf.regexp_extract('str', r'(\\d+)', 1)).show()\n    +---+-----------------------------+\n    |str|regexp_extract(str, (\\d+), 1)|\n    +---+-----------------------------+\n    |foo|                             |\n    +---+-----------------------------+\n\n    >>> df = spark.createDataFrame([('aaaac',)], ['str'])\n    >>> df.select('*', sf.regexp_extract(sf.col('str'), '(a+)(b)?(c)', 2)).show()\n    +-----+-----------------------------------+\n    |  str|regexp_extract(str, (a+)(b)?(c), 2)|\n    +-----+-----------------------------------+\n    |aaaac|                                   |\n    +-----+-----------------------------------+\n    ",
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "pattern",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "text",
      },
      {
        name: "idx",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  regexp_extract_all: {
    doc: "Extract all strings in the `str` that match the Java regex `regexp`\n    and corresponding to the regex group index.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    regexp : :class:`~pyspark.sql.Column` or column name\n        regex pattern to apply.\n    idx : :class:`~pyspark.sql.Column` or int, optional\n        matched group id.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        all strings in the `str` that match a Java regex and corresponding to the regex group index.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.regexp_extract`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([(\"100-200, 300-400\", r\"(\\d+)-(\\d+)\")], [\"str\", \"regexp\"])\n    >>> df.select('*', sf.regexp_extract_all('str', sf.lit(r'(\\d+)-(\\d+)'))).show()\n    +----------------+-----------+---------------------------------------+\n    |             str|     regexp|regexp_extract_all(str, (\\d+)-(\\d+), 1)|\n    +----------------+-----------+---------------------------------------+\n    |100-200, 300-400|(\\d+)-(\\d+)|                             [100, 300]|\n    +----------------+-----------+---------------------------------------+\n\n    >>> df.select('*', sf.regexp_extract_all('str', sf.lit(r'(\\d+)-(\\d+)'), sf.lit(1))).show()\n    +----------------+-----------+---------------------------------------+\n    |             str|     regexp|regexp_extract_all(str, (\\d+)-(\\d+), 1)|\n    +----------------+-----------+---------------------------------------+\n    |100-200, 300-400|(\\d+)-(\\d+)|                             [100, 300]|\n    +----------------+-----------+---------------------------------------+\n\n    >>> df.select('*', sf.regexp_extract_all('str', sf.lit(r'(\\d+)-(\\d+)'), 2)).show()\n    +----------------+-----------+---------------------------------------+\n    |             str|     regexp|regexp_extract_all(str, (\\d+)-(\\d+), 2)|\n    +----------------+-----------+---------------------------------------+\n    |100-200, 300-400|(\\d+)-(\\d+)|                             [200, 400]|\n    +----------------+-----------+---------------------------------------+\n\n    >>> df.select('*', sf.regexp_extract_all('str', sf.col(\"regexp\"))).show()\n    +----------------+-----------+----------------------------------+\n    |             str|     regexp|regexp_extract_all(str, regexp, 1)|\n    +----------------+-----------+----------------------------------+\n    |100-200, 300-400|(\\d+)-(\\d+)|                        [100, 300]|\n    +----------------+-----------+----------------------------------+\n\n    >>> df.select('*', sf.regexp_extract_all(sf.col('str'), \"regexp\")).show()\n    +----------------+-----------+----------------------------------+\n    |             str|     regexp|regexp_extract_all(str, regexp, 1)|\n    +----------------+-----------+----------------------------------+\n    |100-200, 300-400|(\\d+)-(\\d+)|                        [100, 300]|\n    +----------------+-----------+----------------------------------+\n    ",
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "regexp",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "idx",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  regexp_replace: {
    doc: 'Replace all substrings of the specified string value that match regexp with replacement.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    string : :class:`~pyspark.sql.Column` or str\n        column name or column containing the string value\n    pattern : :class:`~pyspark.sql.Column` or str\n        column object or str containing the regexp pattern\n    replacement : :class:`~pyspark.sql.Column` or str\n        column object or str containing the replacement\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        string with all substrings replaced.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(\n    ...      [("100-200", r"(\\d+)", "--")],\n    ...      ["str", "pattern", "replacement"]\n    ... )\n\n    Example 1: Replaces all the substrings in the `str` column name that\n    match the regex pattern `(\\d+)` (one or more digits) with the replacement\n    string "--".\n\n    >>> df.select(\'*\', sf.regexp_replace(\'str\', r\'(\\d+)\', \'--\')).show()\n    +-------+-------+-----------+---------------------------------+\n    |    str|pattern|replacement|regexp_replace(str, (\\d+), --, 1)|\n    +-------+-------+-----------+---------------------------------+\n    |100-200|  (\\d+)|         --|                            -----|\n    +-------+-------+-----------+---------------------------------+\n\n    Example 2: Replaces all the substrings in the `str` Column that match\n    the regex pattern in the `pattern` Column with the string in the `replacement`\n    column.\n\n    >>> df.select(\'*\', \\\n    ...     sf.regexp_replace(sf.col("str"), sf.col("pattern"), sf.col("replacement")) \\\n    ... ).show()\n    +-------+-------+-----------+--------------------------------------------+\n    |    str|pattern|replacement|regexp_replace(str, pattern, replacement, 1)|\n    +-------+-------+-----------+--------------------------------------------+\n    |100-200|  (\\d+)|         --|                                       -----|\n    +-------+-------+-----------+--------------------------------------------+\n    ',
    group: "string",
    args: [
      {
        name: "string",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "pattern",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "replacement",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  reverse: {
    doc: "\n    Collection function: returns a reversed string or an array with elements in reverse order.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The name of the column or an expression that represents the element to be reversed.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that contains a reversed string or an array with elements in reverse order.\n\n    Examples\n    --------\n    Example 1: Reverse a string\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('Spark SQL',)], ['data'])\n    >>> df.select(sf.reverse(df.data)).show()\n    +-------------+\n    |reverse(data)|\n    +-------------+\n    |    LQS krapS|\n    +-------------+\n\n    Example 2: Reverse an array\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([2, 1, 3],) ,([1],) ,([],)], ['data'])\n    >>> df.select(sf.reverse(df.data)).show()\n    +-------------+\n    |reverse(data)|\n    +-------------+\n    |    [3, 1, 2]|\n    |          [1]|\n    |           []|\n    +-------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  round: {
    doc: "\n    Round the given value to `scale` decimal places using HALF_UP rounding mode if `scale` >= 0\n    or at integral part when `scale` < 0.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        The target column or column name to compute the round on.\n    scale : :class:`~pyspark.sql.Column` or int, optional\n        An optional parameter to control the rounding behavior.\n\n        .. versionchanged:: 4.0.0\n            Support Column type.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A column for the rounded value.\n\n    Examples\n    --------\n    Example 1: Compute the rounded of a column value\n\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.round(sf.lit(2.5))).show()\n    +-------------+\n    |round(2.5, 0)|\n    +-------------+\n    |          3.0|\n    +-------------+\n\n    Example 2: Compute the rounded of a column value with a specified scale\n\n    >>> import pyspark.sql.functions as sf\n    >>> spark.range(1).select(sf.round(sf.lit(2.1267), sf.lit(2))).show()\n    +----------------+\n    |round(2.1267, 2)|\n    +----------------+\n    |            2.13|\n    +----------------+\n    ",
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "scale",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  rpad: {
    doc: "\n    Right-pad the string column to width `len` with `pad`.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        target column to work on.\n    len : :class:`~pyspark.sql.Column` or int\n        length of the final string.\n\n        .. versionchanged:: 4.0.0\n             `pattern` now accepts column.\n\n    pad : :class:`~pyspark.sql.Column` or literal string\n        chars to prepend.\n\n        .. versionchanged:: 4.0.0\n             `pattern` now accepts column.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        right padded result.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.lpad`\n\n    Examples\n    --------\n    Example 1: Pad with a literal string\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('abcd',), ('xyz',), ('12',)], ['s',])\n    >>> df.select(\"*\", sf.rpad(df.s, 6, '#')).show()\n    +----+-------------+\n    |   s|rpad(s, 6, #)|\n    +----+-------------+\n    |abcd|       abcd##|\n    | xyz|       xyz###|\n    |  12|       12####|\n    +----+-------------+\n\n    Example 2: Pad with a bytes column\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('abcd',), ('xyz',), ('12',)], ['s',])\n    >>> df.select(\"*\", sf.rpad(df.s, 6, sf.lit(b\"uv\"))).show()\n    +----+-------------------+\n    |   s|rpad(s, 6, X'7576')|\n    +----+-------------------+\n    |abcd|             abcduv|\n    | xyz|             xyzuvu|\n    |  12|             12uvuv|\n    +----+-------------------+\n    ",
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "len",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
      {
        name: "pad",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  rtrim: {
    doc: '\n    Trim the spaces from right end for the specified string value.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    trim : :class:`~pyspark.sql.Column` or column name, optional\n        The trim string characters to trim, the default value is a single space\n\n        .. versionadded:: 4.0.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        right trimmed values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.trim`\n    :meth:`pyspark.sql.functions.ltrim`\n\n    Examples\n    --------\n    Example 1: Trim the spaces\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["   Spark", "Spark  ", " Spark"], "STRING")\n    >>> df.select("*", sf.rtrim("value")).show()\n    +--------+------------+\n    |   value|rtrim(value)|\n    +--------+------------+\n    |   Spark|       Spark|\n    | Spark  |       Spark|\n    |   Spark|       Spark|\n    +--------+------------+\n\n    Example 2: Trim specified characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["***Spark", "Spark**", "*Spark"], "STRING")\n    >>> df.select("*", sf.rtrim("value", sf.lit("*"))).show()\n    +--------+---------------------------+\n    |   value|TRIM(TRAILING * FROM value)|\n    +--------+---------------------------+\n    |***Spark|                   ***Spark|\n    | Spark**|                      Spark|\n    |  *Spark|                     *Spark|\n    +--------+---------------------------+\n\n    Example 3: Trim a column containing different characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("**Spark*", "*"), ("==Spark=", "=")], ["value", "t"])\n    >>> df.select("*", sf.rtrim("value", "t")).show()\n    +--------+---+---------------------------+\n    |   value|  t|TRIM(TRAILING t FROM value)|\n    +--------+---+---------------------------+\n    |**Spark*|  *|                    **Spark|\n    |==Spark=|  =|                    ==Spark|\n    +--------+---+---------------------------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "trim",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  sha1: {
    doc: "Returns the hex string result of SHA-1.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        the column for computed results.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.sha`\n    :meth:`pyspark.sql.functions.sha2`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('ABC',)], ['a'])\n    >>> df.select('*', sf.sha1('a')).show(truncate=False)\n    +---+----------------------------------------+\n    |a  |sha1(a)                                 |\n    +---+----------------------------------------+\n    |ABC|3c01bdbb26f358bab27f267924aa2c9a03fcfdb8|\n    +---+----------------------------------------+\n    ",
    group: "misc",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: [
          "short",
          "integer",
          "long",
          "float",
          "double",
          "decimal",
          "string",
          "date",
          "timestamp",
          "array<.*>",
        ],
        custom_input: "nan",
      },
    ],
  },
  shuffle: {
    doc: '\n    Array function: Generates a random permutation of the given array.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        The name of the column or expression to be shuffled.\n    seed : :class:`~pyspark.sql.Column` or int, optional\n        Seed value for the random generator.\n\n        .. versionadded:: 4.0.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new column that contains an array of elements in random order.\n\n    Notes\n    -----\n    The `shuffle` function is non-deterministic, meaning the order of the output array\n    can be different for each execution.\n\n    Examples\n    --------\n    Example 1: Shuffling a simple array\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.sql("SELECT ARRAY(1, 20, 3, 5) AS data")\n    >>> df.select("*", sf.shuffle(df.data, sf.lit(123))).show()\n    +-------------+-------------+\n    |         data|shuffle(data)|\n    +-------------+-------------+\n    |[1, 20, 3, 5]|[5, 1, 20, 3]|\n    +-------------+-------------+\n\n    Example 2: Shuffling an array with null values\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.sql("SELECT ARRAY(1, 20, NULL, 5) AS data")\n    >>> df.select("*", sf.shuffle(sf.col("data"), 234)).show()\n    +----------------+----------------+\n    |            data|   shuffle(data)|\n    +----------------+----------------+\n    |[1, 20, NULL, 5]|[NULL, 5, 20, 1]|\n    +----------------+----------------+\n\n    Example 3: Shuffling an array with duplicate values\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.sql("SELECT ARRAY(1, 2, 2, 3, 3, 3) AS data")\n    >>> df.select("*", sf.shuffle("data", 345)).show()\n    +------------------+------------------+\n    |              data|     shuffle(data)|\n    +------------------+------------------+\n    |[1, 2, 2, 3, 3, 3]|[2, 3, 3, 1, 2, 3]|\n    +------------------+------------------+\n\n    Example 4: Shuffling an array with random seed\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.sql("SELECT ARRAY(1, 2, 2, 3, 3, 3) AS data")\n    >>> df.select("*", sf.shuffle("data")).show() # doctest: +SKIP\n    +------------------+------------------+\n    |              data|     shuffle(data)|\n    +------------------+------------------+\n    |[1, 2, 2, 3, 3, 3]|[3, 3, 2, 3, 2, 1]|\n    +------------------+------------------+\n    ',
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "seed",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  sin: {
    doc: '\n    Computes sine of the input column.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        sine of the angle, as if computed by `java.lang.Math.sin()`\n\n    Examples\n    --------\n    Example 1: Compute the sine\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (0.0), (PI() / 2), (PI() / 4) AS TAB(value)"\n    ... ).select("*", sf.sin("value")).show()\n    +------------------+------------------+\n    |             value|        SIN(value)|\n    +------------------+------------------+\n    |               0.0|               0.0|\n    |1.5707963267948...|               1.0|\n    |0.7853981633974...|0.7071067811865...|\n    +------------------+------------------+\n\n    Example 2: Compute the sine of invalid values\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (FLOAT(\'NAN\')), (NULL) AS TAB(value)"\n    ... ).select("*", sf.sin("value")).show()\n    +-----+----------+\n    |value|SIN(value)|\n    +-----+----------+\n    |  NaN|       NaN|\n    | NULL|      NULL|\n    +-----+----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  size: {
    doc: "\n    Collection function: returns the length of the array or map stored in the column.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        name of column or expression\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        length of the array/map.\n\n    Examples\n    --------\n    >>> df = spark.createDataFrame([([1, 2, 3],),([1],),([],)], ['data'])\n    >>> df.select(size(df.data)).collect()\n    [Row(size(data)=3), Row(size(data)=1), Row(size(data)=0)]\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
    ],
  },
  slice: {
    doc: "\n    Array function: Returns a new array column by slicing the input array column from\n    a start index to a specific length. The indices start at 1, and can be negative to index\n    from the end of the array. The length specifies the number of elements in the resulting array.\n\n    .. versionadded:: 2.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    x : :class:`~pyspark.sql.Column` or str\n        Input array column or column name to be sliced.\n    start : :class:`~pyspark.sql.Column`, str, or int\n        The start index for the slice operation. If negative, starts the index from the\n        end of the array.\n    length : :class:`~pyspark.sql.Column`, str, or int\n        The length of the slice, representing number of elements in the resulting array.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        A new Column object of Array type, where each value is a slice of the corresponding\n        list from the input column.\n\n    Examples\n    --------\n    Example 1: Basic usage of the slice function.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],), ([4, 5],)], ['x'])\n    >>> df.select(sf.slice(df.x, 2, 2)).show()\n    +--------------+\n    |slice(x, 2, 2)|\n    +--------------+\n    |        [2, 3]|\n    |           [5]|\n    +--------------+\n\n    Example 2: Slicing with negative start index.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3],), ([4, 5],)], ['x'])\n    >>> df.select(sf.slice(df.x, -1, 1)).show()\n    +---------------+\n    |slice(x, -1, 1)|\n    +---------------+\n    |            [3]|\n    |            [5]|\n    +---------------+\n\n    Example 3: Slice function with column inputs for start and length.\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([([1, 2, 3], 2, 2), ([4, 5], 1, 3)], ['x', 'start', 'length'])\n    >>> df.select(sf.slice(df.x, df.start, df.length)).show()\n    +-----------------------+\n    |slice(x, start, length)|\n    +-----------------------+\n    |                 [2, 3]|\n    |                 [4, 5]|\n    +-----------------------+\n    ",
    group: "array",
    args: [
      {
        name: "x",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "start",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
      {
        name: "length",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  sort_array: {
    doc: "\n    Array function: Sorts the input array in ascending or descending order according\n    to the natural ordering of the array elements. Null elements will be placed at the beginning\n    of the returned array in ascending order or at the end of the returned array in descending\n    order.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or str\n        Name of the column or expression.\n    asc : bool, optional\n        Whether to sort in ascending or descending order. If `asc` is True (default),\n        then the sorting is in ascending order. If False, then in descending order.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        Sorted array.\n\n    Examples\n    --------\n    Example 1: Sorting an array in ascending order\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([([2, 1, None, 3],)], ['data'])\n    >>> df.select(sf.sort_array(df.data)).show()\n    +----------------------+\n    |sort_array(data, true)|\n    +----------------------+\n    |       [NULL, 1, 2, 3]|\n    +----------------------+\n\n    Example 2: Sorting an array in descending order\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([([2, 1, None, 3],)], ['data'])\n    >>> df.select(sf.sort_array(df.data, asc=False)).show()\n    +-----------------------+\n    |sort_array(data, false)|\n    +-----------------------+\n    |        [3, 2, 1, NULL]|\n    +-----------------------+\n\n    Example 3: Sorting an array with a single element\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([([1],)], ['data'])\n    >>> df.select(sf.sort_array(df.data)).show()\n    +----------------------+\n    |sort_array(data, true)|\n    +----------------------+\n    |                   [1]|\n    +----------------------+\n\n    Example 4: Sorting an empty array\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, StringType, StructField, StructType\n    >>> schema = StructType([StructField(\"data\", ArrayType(StringType()), True)])\n    >>> df = spark.createDataFrame([([],)], schema=schema)\n    >>> df.select(sf.sort_array(df.data)).show()\n    +----------------------+\n    |sort_array(data, true)|\n    +----------------------+\n    |                    []|\n    +----------------------+\n\n    Example 5: Sorting an array with null values\n\n    >>> from pyspark.sql import functions as sf\n    >>> from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField\n    >>> schema = StructType([StructField(\"data\", ArrayType(IntegerType()), True)])\n    >>> df = spark.createDataFrame([([None, None, None],)], schema=schema)\n    >>> df.select(sf.sort_array(df.data)).show()\n    +----------------------+\n    |sort_array(data, true)|\n    +----------------------+\n    |    [NULL, NULL, NULL]|\n    +----------------------+\n    ",
    group: "array",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["array<.*>"],
        custom_input: "nan",
      },
      {
        name: "asc",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "checkbox",
      },
    ],
  },
  split: {
    doc: "\n    Splits str around matches of the given pattern.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        a string expression to split\n    pattern : :class:`~pyspark.sql.Column` or literal string\n        a string representing a regular expression. The regex string should be\n        a Java regular expression.\n\n        .. versionchanged:: 4.0.0\n             `pattern` now accepts column. Does not accept column name since string type remain\n             accepted as a regular expression representation, for backwards compatibility.\n             In addition to int, `limit` now accepts column and column name.\n\n    limit : :class:`~pyspark.sql.Column` or column name or int\n        an integer which controls the number of times `pattern` is applied.\n\n        * ``limit > 0``: The resulting array's length will not be more than `limit`, and the\n                         resulting array's last entry will contain all input beyond the last\n                         matched pattern.\n        * ``limit <= 0``: `pattern` will be applied as many times as possible, and the resulting\n                          array can be of any size.\n\n        .. versionchanged:: 3.0\n           `split` now takes an optional `limit` field. If not provided, default limit value is -1.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        array of separated strings.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.sentences`\n    :meth:`pyspark.sql.functions.split_part`\n\n    Examples\n    --------\n    Example 1: Repeat with a constant pattern\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('oneAtwoBthreeC',)], ['s',])\n    >>> df.select('*', sf.split(df.s, '[ABC]')).show()\n    +--------------+-------------------+\n    |             s|split(s, [ABC], -1)|\n    +--------------+-------------------+\n    |oneAtwoBthreeC|[one, two, three, ]|\n    +--------------+-------------------+\n\n    >>> df.select('*', sf.split(df.s, '[ABC]', 2)).show()\n    +--------------+------------------+\n    |             s|split(s, [ABC], 2)|\n    +--------------+------------------+\n    |oneAtwoBthreeC| [one, twoBthreeC]|\n    +--------------+------------------+\n\n    >>> df.select('*', sf.split('s', '[ABC]', -2)).show()\n    +--------------+-------------------+\n    |             s|split(s, [ABC], -2)|\n    +--------------+-------------------+\n    |oneAtwoBthreeC|[one, two, three, ]|\n    +--------------+-------------------+\n\n    Example 2: Repeat with a column containing different patterns and limits\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([\n    ...     ('oneAtwoBthreeC', '[ABC]', 2),\n    ...     ('1A2B3C', '[1-9]+', 1),\n    ...     ('aa2bb3cc4', '[1-9]+', -1)], ['s', 'p', 'l'])\n    >>> df.select('*', sf.split(df.s, df.p)).show()\n    +--------------+------+---+-------------------+\n    |             s|     p|  l|    split(s, p, -1)|\n    +--------------+------+---+-------------------+\n    |oneAtwoBthreeC| [ABC]|  2|[one, two, three, ]|\n    |        1A2B3C|[1-9]+|  1|        [, A, B, C]|\n    |     aa2bb3cc4|[1-9]+| -1|     [aa, bb, cc, ]|\n    +--------------+------+---+-------------------+\n\n    >>> df.select(sf.split('s', df.p, 'l')).show()\n    +-----------------+\n    |   split(s, p, l)|\n    +-----------------+\n    |[one, twoBthreeC]|\n    |         [1A2B3C]|\n    |   [aa, bb, cc, ]|\n    +-----------------+\n    ",
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "pattern",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "limit",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  sqrt: {
    doc: '\n    Computes the square root of the specified float value.\n\n    .. versionadded:: 1.3.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to compute on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        column for computed results.\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (-1), (0), (1), (4), (NULL) AS TAB(value)"\n    ... ).select("*", sf.sqrt("value")).show()\n    +-----+-----------+\n    |value|SQRT(value)|\n    +-----+-----------+\n    |   -1|        NaN|\n    |    0|        0.0|\n    |    1|        1.0|\n    |    4|        2.0|\n    | NULL|       NULL|\n    +-----+-----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  startswith: {
    doc: '\n    Returns a boolean. The value is True if str starts with prefix.\n    Returns NULL if either input expression is NULL. Otherwise, returns False.\n    Both str or prefix must be of STRING or BINARY type.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or str\n        A column of string.\n    prefix : :class:`~pyspark.sql.Column` or str\n        A column of string, the prefix.\n\n    Examples\n    --------\n    >>> df = spark.createDataFrame([("Spark SQL", "Spark",)], ["a", "b"])\n    >>> df.select(startswith(df.a, df.b).alias(\'r\')).collect()\n    [Row(r=True)]\n\n    >>> df = spark.createDataFrame([("414243", "4142",)], ["e", "f"])\n    >>> df = df.select(to_binary("e").alias("e"), to_binary("f").alias("f"))\n    >>> df.printSchema()\n    root\n     |-- e: binary (nullable = true)\n     |-- f: binary (nullable = true)\n    >>> df.select(startswith("e", "f"), startswith("f", "e")).show()\n    +----------------+----------------+\n    |startswith(e, f)|startswith(f, e)|\n    +----------------+----------------+\n    |            true|           false|\n    +----------------+----------------+\n    ',
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "prefix",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  substring: {
    doc: "\n    Substring starts at `pos` and is of length `len` when str is String type or\n    returns the slice of byte array that starts at `pos` in byte and is of length `len`\n    when str is Binary type.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Notes\n    -----\n    The position is not zero based, but 1 based index.\n\n    Parameters\n    ----------\n    str : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    pos : :class:`~pyspark.sql.Column` or column name or int\n        starting position in str.\n\n        .. versionchanged:: 4.0.0\n            `pos` now accepts column and column name.\n\n    len : :class:`~pyspark.sql.Column` or column name or int\n        length of chars.\n\n        .. versionchanged:: 4.0.0\n            `len` now accepts column and column name.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        substring of given value.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.instr`\n    :meth:`pyspark.sql.functions.locate`\n    :meth:`pyspark.sql.functions.substr`\n    :meth:`pyspark.sql.functions.substring_index`\n    :meth:`pyspark.sql.Column.substr`\n\n    Examples\n    --------\n    Example 1: Using literal integers as arguments\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('abcd',)], ['s',])\n    >>> df.select('*', sf.substring(df.s, 1, 2)).show()\n    +----+------------------+\n    |   s|substring(s, 1, 2)|\n    +----+------------------+\n    |abcd|                ab|\n    +----+------------------+\n\n    Example 2: Using columns as arguments\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('Spark', 2, 3)], ['s', 'p', 'l'])\n    >>> df.select('*', sf.substring(df.s, 2, df.l)).show()\n    +-----+---+---+------------------+\n    |    s|  p|  l|substring(s, 2, l)|\n    +-----+---+---+------------------+\n    |Spark|  2|  3|               par|\n    +-----+---+---+------------------+\n\n    >>> df.select('*', sf.substring(df.s, df.p, 3)).show()\n    +-----+---+---+------------------+\n    |    s|  p|  l|substring(s, p, 3)|\n    +-----+---+---+------------------+\n    |Spark|  2|  3|               par|\n    +-----+---+---+------------------+\n\n    >>> df.select('*', sf.substring(df.s, df.p, df.l)).show()\n    +-----+---+---+------------------+\n    |    s|  p|  l|substring(s, p, l)|\n    +-----+---+---+------------------+\n    |Spark|  2|  3|               par|\n    +-----+---+---+------------------+\n\n    Example 3: Using column names as arguments\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('Spark', 2, 3)], ['s', 'p', 'l'])\n    >>> df.select('*', sf.substring(df.s, 2, 'l')).show()\n    +-----+---+---+------------------+\n    |    s|  p|  l|substring(s, 2, l)|\n    +-----+---+---+------------------+\n    |Spark|  2|  3|               par|\n    +-----+---+---+------------------+\n\n    >>> df.select('*', sf.substring('s', 'p', 'l')).show()\n    +-----+---+---+------------------+\n    |    s|  p|  l|substring(s, p, l)|\n    +-----+---+---+------------------+\n    |Spark|  2|  3|               par|\n    +-----+---+---+------------------+\n    ",
    group: "string",
    args: [
      {
        name: "str",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "pos",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
      {
        name: "len",
        selector: "single",
        type: "input",
        spark_types: [],
        custom_input: "number",
      },
    ],
  },
  tan: {
    doc: '\n    Computes tangent of the input column.\n\n    .. versionadded:: 1.4.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        angle in radians\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        tangent of the given value, as if computed by `java.lang.Math.tan()`\n\n    Examples\n    --------\n    Example 1: Compute the tangent\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (0.0), (PI() / 4), (PI() / 6) AS TAB(value)"\n    ... ).select("*", sf.tan("value")).show()\n    +------------------+------------------+\n    |             value|        TAN(value)|\n    +------------------+------------------+\n    |               0.0|               0.0|\n    |0.7853981633974...|0.9999999999999...|\n    |0.5235987755982...|0.5773502691896...|\n    +------------------+------------------+\n\n    Example 2: Compute the tangent of invalid values\n\n    >>> from pyspark.sql import functions as sf\n    >>> spark.sql(\n    ...     "SELECT * FROM VALUES (FLOAT(\'NAN\')), (NULL) AS TAB(value)"\n    ... ).select("*", sf.tan("value")).show()\n    +-----+----------+\n    |value|TAN(value)|\n    +-----+----------+\n    |  NaN|       NaN|\n    | NULL|      NULL|\n    +-----+----------+\n    ',
    group: "math",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["short", "integer", "long", "float", "double", "decimal"],
        custom_input: "number",
      },
    ],
  },
  to_unix_timestamp: {
    doc: "\n    Returns the UNIX timestamp of the given time.\n\n    .. versionadded:: 3.5.0\n\n    Parameters\n    ----------\n    timestamp : :class:`~pyspark.sql.Column` or column name\n        Input column or strings.\n    format : :class:`~pyspark.sql.Column` or column name, optional\n        format to use to convert UNIX timestamp values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.to_date`\n    :meth:`pyspark.sql.functions.to_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp_ltz`\n    :meth:`pyspark.sql.functions.to_timestamp_ntz`\n    :meth:`pyspark.sql.functions.to_utc_timestamp`\n\n    Examples\n    --------\n    >>> spark.conf.set(\"spark.sql.session.timeZone\", \"America/Los_Angeles\")\n\n    Example 1: Using default format to parse the timestamp string.\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 12:12:12',)], ['ts'])\n    >>> df.select('*', sf.to_unix_timestamp('ts')).show()\n    +-------------------+------------------------------------------+\n    |                 ts|to_unix_timestamp(ts, yyyy-MM-dd HH:mm:ss)|\n    +-------------------+------------------------------------------+\n    |2015-04-08 12:12:12|                                1428520332|\n    +-------------------+------------------------------------------+\n\n    Example 2: Using user-specified format 'yyyy-MM-dd' to parse the date string.\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',)], ['dt'])\n    >>> df.select('*', sf.to_unix_timestamp(df.dt, sf.lit('yyyy-MM-dd'))).show()\n    +----------+---------------------------------+\n    |        dt|to_unix_timestamp(dt, yyyy-MM-dd)|\n    +----------+---------------------------------+\n    |2015-04-08|                       1428476400|\n    +----------+---------------------------------+\n\n    Example 3: Using a format column to represent different formats.\n\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame(\n    ...     [('2015-04-08', 'yyyy-MM-dd'), ('2025+01+09', 'yyyy+MM+dd')], ['dt', 'fmt'])\n    >>> df.select('*', sf.to_unix_timestamp('dt', 'fmt')).show()\n    +----------+----------+--------------------------+\n    |        dt|       fmt|to_unix_timestamp(dt, fmt)|\n    +----------+----------+--------------------------+\n    |2015-04-08|yyyy-MM-dd|                1428476400|\n    |2025+01+09|yyyy+MM+dd|                1736409600|\n    +----------+----------+--------------------------+\n\n    >>> spark.conf.unset(\"spark.sql.session.timeZone\")\n    ",
    group: "date",
    args: [
      {
        name: "timestamp",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "format",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  to_utc_timestamp: {
    doc: "\n    This is a common function for databases supporting TIMESTAMP WITHOUT TIMEZONE. This function\n    takes a timestamp which is timezone-agnostic, and interprets it as a timestamp in the given\n    timezone, and renders that timestamp as a timestamp in UTC.\n\n    However, timestamp in Spark represents number of microseconds from the Unix epoch, which is not\n    timezone-agnostic. So in Spark this function just shift the timestamp value from the given\n    timezone to UTC timezone.\n\n    This function may return confusing result if the input is a string with timezone, e.g.\n    '2018-03-13T06:18:23+00:00'. The reason is that, Spark firstly cast the string to timestamp\n    according to the timezone in the string, and finally display the result by converting the\n    timestamp to string according to the session local timezone.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    timestamp : :class:`~pyspark.sql.Column` or column name\n        the column that contains timestamps\n    tz : :class:`~pyspark.sql.Column` or literal string\n        A string detailing the time zone ID that the input should be adjusted to. It should\n        be in the format of either region-based zone IDs or zone offsets. Region IDs must\n        have the form 'area/city', such as 'America/Los_Angeles'. Zone offsets must be in\n        the format '(+|-)HH:mm', for example '-08:00' or '+01:00'. Also 'UTC' and 'Z' are\n        supported as aliases of '+00:00'. Other short names are not recommended to use\n        because they can be ambiguous.\n\n        .. versionchanged:: 2.4.0\n           `tz` can take a :class:`~pyspark.sql.Column` containing timezone ID strings.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        timestamp value represented in UTC timezone.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.from_utc_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp`\n    :meth:`pyspark.sql.functions.to_timestamp_ltz`\n    :meth:`pyspark.sql.functions.to_timestamp_ntz`\n\n    Examples\n    --------\n    >>> import pyspark.sql.functions as sf\n    >>> df = spark.createDataFrame([('1997-02-28 10:30:00', 'JST')], ['ts', 'tz'])\n    >>> df.select('*', sf.to_utc_timestamp('ts', \"PST\")).show()\n    +-------------------+---+-------------------------+\n    |                 ts| tz|to_utc_timestamp(ts, PST)|\n    +-------------------+---+-------------------------+\n    |1997-02-28 10:30:00|JST|      1997-02-28 18:30:00|\n    +-------------------+---+-------------------------+\n\n    >>> df.select('*', sf.to_utc_timestamp(df.ts, df.tz)).show()\n    +-------------------+---+------------------------+\n    |                 ts| tz|to_utc_timestamp(ts, tz)|\n    +-------------------+---+------------------------+\n    |1997-02-28 10:30:00|JST|     1997-02-28 01:30:00|\n    +-------------------+---+------------------------+\n    ",
    group: "date",
    args: [
      {
        name: "timestamp",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "tz",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  trim: {
    doc: '\n    Trim the spaces from both ends for the specified string column.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n    trim : :class:`~pyspark.sql.Column` or column name, optional\n        The trim string characters to trim, the default value is a single space\n\n        .. versionadded:: 4.0.0\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        trimmed values from both sides.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.ltrim`\n    :meth:`pyspark.sql.functions.rtrim`\n\n    Examples\n    --------\n    Example 1: Trim the spaces\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["   Spark", "Spark  ", " Spark"], "STRING")\n    >>> df.select("*", sf.trim("value")).show()\n    +--------+-----------+\n    |   value|trim(value)|\n    +--------+-----------+\n    |   Spark|      Spark|\n    | Spark  |      Spark|\n    |   Spark|      Spark|\n    +--------+-----------+\n\n    Example 2: Trim specified characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["***Spark", "Spark**", "*Spark"], "STRING")\n    >>> df.select("*", sf.trim("value", sf.lit("*"))).show()\n    +--------+-----------------------+\n    |   value|TRIM(BOTH * FROM value)|\n    +--------+-----------------------+\n    |***Spark|                  Spark|\n    | Spark**|                  Spark|\n    |  *Spark|                  Spark|\n    +--------+-----------------------+\n\n    Example 3: Trim a column containing different characters\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([("**Spark*", "*"), ("==Spark=", "=")], ["value", "t"])\n    >>> df.select("*", sf.trim("value", "t")).show()\n    +--------+---+-----------------------+\n    |   value|  t|TRIM(BOTH t FROM value)|\n    +--------+---+-----------------------+\n    |**Spark*|  *|                  Spark|\n    |==Spark=|  =|                  Spark|\n    +--------+---+-----------------------+\n    ',
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
      {
        name: "trim",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  trunc: {
    doc: "\n    Returns date truncated to the unit specified by the format.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    date : :class:`~pyspark.sql.Column` or column name\n        input column of values to truncate.\n    format : literal string\n        'year', 'yyyy', 'yy' to truncate by year,\n        or 'month', 'mon', 'mm' to truncate by month\n        Other options are: 'week', 'quarter'\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        truncated date.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.date_trunc`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('1997-02-28',)], ['dt'])\n    >>> df.select('*', sf.trunc(df.dt, 'year')).show()\n    +----------+---------------+\n    |        dt|trunc(dt, year)|\n    +----------+---------------+\n    |1997-02-28|     1997-01-01|\n    +----------+---------------+\n\n    >>> df.select('*', sf.trunc('dt', 'mon')).show()\n    +----------+--------------+\n    |        dt|trunc(dt, mon)|\n    +----------+--------------+\n    |1997-02-28|    1997-02-01|\n    +----------+--------------+\n    ",
    group: "date",
    args: [
      {
        name: "date",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
      {
        name: "format",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  upper: {
    doc: '\n    Converts a string expression to upper case.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        upper case values.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.lower`\n\n    Examples\n    --------\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame(["Spark", "PySpark", "Pandas API"], "STRING")\n    >>> df.select("*", sf.upper("value")).show()\n    +----------+------------+\n    |     value|upper(value)|\n    +----------+------------+\n    |     Spark|       SPARK|\n    |   PySpark|     PYSPARK|\n    |Pandas API|  PANDAS API|\n    +----------+------------+\n    ',
    group: "string",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["string"],
        custom_input: "text",
      },
    ],
  },
  weekofyear: {
    doc: "\n    Extract the week number of a given date as integer.\n    A week is considered to start on a Monday and week 1 is the first week with more than 3 days,\n    as defined by ISO 8601\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        `week` of the year for given date as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.weekday`\n\n    Examples\n    --------\n    Example 1: Extract the week of the year from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.weekofyear('dt')).show()\n    +----------+----------+--------------+\n    |        dt|typeof(dt)|weekofyear(dt)|\n    +----------+----------+--------------+\n    |2015-04-08|    string|            15|\n    |2024-10-31|    string|            44|\n    +----------+----------+--------------+\n\n    Example 2: Extract the week of the year from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.weekofyear('ts')).show()\n    +-------------------+----------+--------------+\n    |                 ts|typeof(ts)|weekofyear(ts)|\n    +-------------------+----------+--------------+\n    |2015-04-08 13:08:15|    string|            15|\n    |2024-10-31 10:09:16|    string|            44|\n    +-------------------+----------+--------------+\n\n    Example 3: Extract the week of the year from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.weekofyear('dt')).show()\n    +----------+----------+--------------+\n    |        dt|typeof(dt)|weekofyear(dt)|\n    +----------+----------+--------------+\n    |2015-04-08|      date|            15|\n    |2024-10-31|      date|            44|\n    +----------+----------+--------------+\n\n    Example 4: Extract the week of the year from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.weekofyear('ts')).show()\n    +-------------------+----------+--------------+\n    |                 ts|typeof(ts)|weekofyear(ts)|\n    +-------------------+----------+--------------+\n    |2015-04-08 13:08:15| timestamp|            15|\n    |2024-10-31 10:09:16| timestamp|            44|\n    +-------------------+----------+--------------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
  year: {
    doc: "\n    Extract the year of a given date/timestamp as integer.\n\n    .. versionadded:: 1.5.0\n\n    .. versionchanged:: 3.4.0\n        Supports Spark Connect.\n\n    Parameters\n    ----------\n    col : :class:`~pyspark.sql.Column` or column name\n        target date/timestamp column to work on.\n\n    Returns\n    -------\n    :class:`~pyspark.sql.Column`\n        year part of the date/timestamp as integer.\n\n    See Also\n    --------\n    :meth:`pyspark.sql.functions.quarter`\n    :meth:`pyspark.sql.functions.month`\n    :meth:`pyspark.sql.functions.day`\n    :meth:`pyspark.sql.functions.hour`\n    :meth:`pyspark.sql.functions.minute`\n    :meth:`pyspark.sql.functions.second`\n    :meth:`pyspark.sql.functions.extract`\n    :meth:`pyspark.sql.functions.datepart`\n    :meth:`pyspark.sql.functions.date_part`\n\n    Examples\n    --------\n    Example 1: Extract the year from a string column representing dates\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08',), ('2024-10-31',)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.year('dt')).show()\n    +----------+----------+--------+\n    |        dt|typeof(dt)|year(dt)|\n    +----------+----------+--------+\n    |2015-04-08|    string|    2015|\n    |2024-10-31|    string|    2024|\n    +----------+----------+--------+\n\n    Example 2: Extract the year from a string column representing timestamp\n\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([('2015-04-08 13:08:15',), ('2024-10-31 10:09:16',)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.year('ts')).show()\n    +-------------------+----------+--------+\n    |                 ts|typeof(ts)|year(ts)|\n    +-------------------+----------+--------+\n    |2015-04-08 13:08:15|    string|    2015|\n    |2024-10-31 10:09:16|    string|    2024|\n    +-------------------+----------+--------+\n\n    Example 3: Extract the year from a date column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.date(2015, 4, 8),),\n    ...     (datetime.date(2024, 10, 31),)], ['dt'])\n    >>> df.select(\"*\", sf.typeof('dt'), sf.year('dt')).show()\n    +----------+----------+--------+\n    |        dt|typeof(dt)|year(dt)|\n    +----------+----------+--------+\n    |2015-04-08|      date|    2015|\n    |2024-10-31|      date|    2024|\n    +----------+----------+--------+\n\n    Example 4: Extract the year from a timestamp column\n\n    >>> import datetime\n    >>> from pyspark.sql import functions as sf\n    >>> df = spark.createDataFrame([\n    ...     (datetime.datetime(2015, 4, 8, 13, 8, 15),),\n    ...     (datetime.datetime(2024, 10, 31, 10, 9, 16),)], ['ts'])\n    >>> df.select(\"*\", sf.typeof('ts'), sf.year('ts')).show()\n    +-------------------+----------+--------+\n    |                 ts|typeof(ts)|year(ts)|\n    +-------------------+----------+--------+\n    |2015-04-08 13:08:15| timestamp|    2015|\n    |2024-10-31 10:09:16| timestamp|    2024|\n    +-------------------+----------+--------+\n    ",
    group: "date",
    args: [
      {
        name: "col",
        selector: "single",
        type: "column",
        spark_types: ["date", "timestamp"],
        custom_input: "text",
      },
    ],
  },
};
