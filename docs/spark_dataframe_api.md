1. Summary == df.count()

2. Filter:

   - Number/Date

     - 2 == 2
     - 2 > 2
     - 2 < 2
     - 2 >= 2
     - 2 <= 2
     - between(2, 4)

   - Text

     - contains('Spark SQL', 'Spark')
     - ilike('Spark', '\_Park')
       - \_ matches any one character in the input (similar to . in posix regular expressions)
       - % matches zero or more characters in the input (similar to .\* in posix regular expressions)
     - rlike('%SystemDrive%\\Users\\John', '%SystemDrive%\\\\Users.\*')
     - startswith('Spark SQL', 'Spark')
     - endswith('Spark SQL', 'SQL')

   - Array:

     - array_contains(array(1, 2, 3), 2)
     - arrays_overlap(array(1, 2, 3), array(3, 4, 5))

   - Null

     - isnull(1)
     - isnotnull(1)

Visualizations:

1. Histogram

sql:
SELECT start_neighborhood, mean(trip_time_in_secs)
FROM <table name>
GROUP BY start_neighborhood

Args:

- x axis,
- y axis,
- agg: Count (number of records), Unique Count, Min, Max, Sum, Mean, Approx. median, Standard Deviation, and Variance
- sorting: true/false

2. Distribution

The distribution board is similar to the histogram, but it displays aggregated data based on ranges of values BUCKETS, rather than specific values

sql:
SELECT X_AXIS_BUCKET_FUNCTION([x-axis-column]), <AGGREGATE_METRIC>([aggregate-column])
FROM <PARENT_BOARD>
GROUP BY X_AXIS_BUCKET_FUNCTION([x-axis-column])

- x axis (NUMERIC COLUMN),
- y axis,
- agg: Count (number of records), Unique Count, Min, Max, Sum, Mean, Approx. median, Standard Deviation, and Variance
- number of buckets
- scale: linear/logarithmic

3. Time series

args:

- x axis (NUMERIC COLUMN),
- y axis,
- agg: Count (number of records), Unique Count, Min, Max, Sum, Mean, Approx. median, Standard Deviation, and Variance
- series: column to divide the data into series. There will be one series (represented as a line in the chart) for each discrete value in the column

4. Chart

- type: bar, horizontal bar, line, scatter, heat grid, pie
- segment by: For chart types other than heat grid and pie, you can also choose to segment the data into series.
- Formatting:
  - change the X- and Y-axis titles,
  - formatting of the axes,
  - legend positioning,
  - series sorting,
  - series colors.
- overlay:
  - you can choose whether the chart should use the data in the current path or from a different dataset.

5. Grid
   The grid board is similar to the histogram, but the grid board aggregates data by two columns rather than one

sql:
SELECT [x-axis-column], [y-axis-column], <AGGREGATE_METRIC>([aggregate-column])
FROM <PARENT_BOARD>
GROUP BY [x-axis-column], [y-axis-column]

args:

- x axis (NUMERIC COLUMN),
- y axis,
- agg: Count (number of records), Unique Count, Min, Max, Sum, Mean, Approx. median, Standard Deviation, and Variance
