export const sparkColumnFunctions = {
  numeric: {
    exprs: {
      abs: {
        desc: "Computes the absolute value.",
        params: [{ name: "column", desc: "target column/value to work on", ptype: "single_col" }],
      },
    },
    sparkTypes: ["short", "integer", "long", "float", "double", "decimal"],
  },
  string: {
    exprs: {
      regexp_extract: {
        desc: "Extract a specific group matched by the Java regex regexp, from the specified string column. If the regex did not match, or the specified group did not match, an empty string is returned",
        params: [
          { name: "column", desc: "target column/value to work on", ptype: "single_col" },
          { name: "patten", desc: "regex pattern to apply", ptype: "text" },
          { name: "idx", desc: "matched group id", ptype: "number" },
        ],
      },
    },
    sparkTypes: ["string"],
  },
  date: {
    exprs: {
      current_date: {
        desc: "Returns the current date at the start of query evaluation as a DateType column. All calls of current_date within the same query return the same value",
        params: [],
      },
    },
    sparkTypes: ["date", "timestamp"],
  },
  array: {
    exprs: {
      array: {
        desc: "Creates a new array column.",
        params: [{ name: "columns", desc: "columns/values that have the same data type", ptype: "multi_col" }],
      },
    },
    sparkTypes: ["array"],
  },
  misc: {
    exprs: {
      isnull: {
        desc: "An expression that returns true if the column is null.",
        params: [{ name: "column", desc: "target column to compute on", ptype: "single_col" }],
      },
    },
    sparkTypes: ["short", "integer", "long", "float", "double", "decimal", "string", "date", "timestamp", "array"],
  },
};
