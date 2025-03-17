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
