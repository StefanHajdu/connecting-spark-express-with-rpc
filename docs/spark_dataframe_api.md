1. Summary == df.count()

2. Filter:

   - Number/Date

     - equal to
       - df.col == val
     - less than
       - df.col < val
     - less than or equal to
       - df.col <= val
     - greater than
       - df.col > val
     - greater than or equal to
       - df.col >= val
     - between
       - SELECT col1 FROM VALUES 1, 3, 5, 7 WHERE col1 BETWEEN 2 AND 5;

   - Text

     - contains
       - SELECT contains('Spark SQL', 'Spark');
     - contains (with wildcard)
     - is (with wildcards)
       - SELECT ilike('Spark', '_Park');
         _ matches any one character in the input (similar to . in posix regular expressions)
         % matches zero or more characters in the input (similar to .\* in posix regular expressions)
     - matches
       - SELECT rlike('%SystemDrive%\\Users\\John', '%SystemDrive%\\\\Users.\*');

   - startswith
   - endswith

   - Array:

     - array contains:
       - SELECT array_contains(array(1, 2, 3), 2)
     - array overlaps:
       - SELECT arrays_overlap(array(1, 2, 3), array(3, 4, 5));

   - Null
     - is null
       - SELECT isnull(1);
     - is not null
       - SELECT isnotnull(1);
