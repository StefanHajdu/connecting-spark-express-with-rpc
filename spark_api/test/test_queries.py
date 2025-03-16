text_filters = [
    {"case": {"expressions": ["contains(domain, 'club')"], "matching": ""}, "correct": 2475},
    {
        "case": {
            "expressions": ["ilike(registrar, 'G_Daddy.com, LLC')"],
            "matching": "",
        },
        "correct": 85127,
    },
    {
        "case": {
            "expressions": ["ilike(registrar, 'GoDaddy.com, LLC')"],
            "matching": "",
        },
        "correct": 85127,
    },
    {
        "case": {
            "expressions": ["ilike(registrar, 'GoDaddy.%, LLC')"],
            "matching": "",
        },
        "correct": 85127,
    },
    {"case": {"expressions": ["ilike(registrar, '成%维数码科技有限公司')"], "matching": ""}, "correct": 340},
    {
        "case": {
            "expressions": ["rlike(domain, '(https?:\/\/)?(www\.)?[a-z0-9-]+\.(com|org)(\.[a-z]{{2,3}})?')"],
            "matching": "",
        },
        "correct": 301352,
    },
    {"case": {"expressions": ["startswith(registrar, 'GoDaddy')"], "matching": ""}, "correct": 93668},
    {"case": {"expressions": ["endswith(registrar, 'com')"], "matching": ""}, "correct": 19551},
    {"case": {"expressions": ["length(registrar) < 10"], "matching": ""}, "correct": 153053},
]

math_numerical_functions = [
    {"expression": "abs(numerical_col)", "col_name": "res"},
    {"expression": "cbrt(numerical_col)", "col_name": "res"},
    {"expression": "ceil(numerical_col)", "col_name": "res"},
    {"expression": "cos(numerical_col)", "col_name": "res"},
    {"expression": "exp(numerical_col)", "col_name": "res"},
    {"expression": "factorial(numerical_col)", "col_name": "res"},
    {"expression": "floor(numerical_col)", "col_name": "res"},
    {"expression": "ln(numerical_col)", "col_name": "res"},
    {"expression": "log(numerical_col)", "col_name": "res"},
    {"expression": "pow(numerical_col, 2)", "col_name": "res"},
    {"expression": "rand(42)", "col_name": "res"},
    {"expression": "round(numerical_col)", "col_name": "res"},
    {"expression": "sin(numerical_col)", "col_name": "res"},
    {"expression": "sqrt(numerical_col)", "col_name": "res"},
    {"expression": "tan(numerical_col)", "col_name": "res"},
]

string_functions = [
    {"expression": "concat(domain, registrar)", "col_name": "res"},
    {"expression": "concat_ws('-', domain, registrar)", "col_name": "res"},
    {"expression": "length(domain)", "col_name": "res"},
    {"expression": "levenshtein(domain, registrar)", "col_name": "res"},
    {"expression": "lower(registrar)", "col_name": "res"},
    {"expression": "lpad(domain, 30, '#')", "col_name": "res"},
    {"expression": "ltrim(domain)", "col_name": "res"},
    {"expression": "regexp_extract(domain, '(\d+)-(\d+)')", "col_name": "res"},
    {"expression": "regexp_replace(domain, '(\d+)', '--')", "col_name": "res"},
    {"expression": "reverse(domain)", "col_name": "res"},
    {"expression": "rpad(domain, 30, '#')", "col_name": "res"},
    {"expression": "rtrim(domain)", "col_name": "res"},
    {"expression": "split(domain, '[a]', 2)", "col_name": "res"},
    {"expression": "substring(domain, 1, 2)", "col_name": "res"},
    {"expression": "trim(registrar)", "col_name": "res"},
    {"expression": "upper(domain)", "col_name": "res"},
]

array_functions = [
    {"expression": "array(domain, registrar)", "col_name": "array_col"},
    {"expression": "array_contains(array_col, 'nasmo.se')", "col_name": "res"},
    {"expression": "element_at(array_col, 1)", "col_name": "res"},
    {"expression": "array_size(array_col)", "col_name": "res"},
    {"expression": "array_join(array_col, '---')", "col_name": "res"},
    {"expression": "array_sort(array_col)", "col_name": "res"},
]
