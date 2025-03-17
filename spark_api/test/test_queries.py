text_filters = [
    {'case': {'expressions': ["contains(domain, 'club')"], 'matching': ''}, 'correct': 2475},
    {
        'case': {
            'expressions': ["ilike(registrar, 'G_Daddy.com, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {
        'case': {
            'expressions': ["ilike(registrar, 'GoDaddy.com, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {
        'case': {
            'expressions': ["ilike(registrar, 'GoDaddy.%, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {'case': {'expressions': ["ilike(registrar, '成%维数码科技有限公司')"], 'matching': ''}, 'correct': 340},
    {
        'case': {
            'expressions': ["rlike(domain, '(https?:\/\/)?(www\.)?[a-z0-9-]+\.(com|org)(\.[a-z]{{2,3}})?')"],
            'matching': '',
        },
        'correct': 301352,
    },
    {'case': {'expressions': ["startswith(registrar, 'GoDaddy')"], 'matching': ''}, 'correct': 93668},
    {'case': {'expressions': ["endswith(registrar, 'com')"], 'matching': ''}, 'correct': 19551},
    {'case': {'expressions': ['length(registrar) < 10'], 'matching': ''}, 'correct': 153053},
]

math_numerical_functions = [
    {'expression': 'abs(numerical_col)', 'col_name': 'res'},
    {'expression': 'cbrt(numerical_col)', 'col_name': 'res'},
    {'expression': 'ceil(numerical_col)', 'col_name': 'res'},
    {'expression': 'cos(numerical_col)', 'col_name': 'res'},
    {'expression': 'exp(numerical_col)', 'col_name': 'res'},
    {'expression': 'factorial(numerical_col)', 'col_name': 'res'},
    {'expression': 'floor(numerical_col)', 'col_name': 'res'},
    {'expression': 'ln(numerical_col)', 'col_name': 'res'},
    {'expression': 'log(numerical_col)', 'col_name': 'res'},
    {'expression': 'pow(numerical_col, 2)', 'col_name': 'res'},
    {'expression': 'rand(42)', 'col_name': 'res'},
    {'expression': 'round(numerical_col)', 'col_name': 'res'},
    {'expression': 'sin(numerical_col)', 'col_name': 'res'},
    {'expression': 'sqrt(numerical_col)', 'col_name': 'res'},
    {'expression': 'tan(numerical_col)', 'col_name': 'res'},
]

string_functions = [
    {'expression': 'concat(domain, registrar)', 'col_name': 'res'},
    {'expression': "concat_ws('-', domain, registrar)", 'col_name': 'res'},
    {'expression': 'length(domain)', 'col_name': 'res'},
    {'expression': 'levenshtein(domain, registrar)', 'col_name': 'res'},
    {'expression': 'lower(registrar)', 'col_name': 'res'},
    {'expression': "lpad(domain, 30, '#')", 'col_name': 'res'},
    {'expression': 'ltrim(domain)', 'col_name': 'res'},
    {'expression': "regexp_extract(domain, '(\d+)-(\d+)')", 'col_name': 'res'},
    {'expression': "regexp_replace(domain, '(\d+)', '--')", 'col_name': 'res'},
    {'expression': 'reverse(domain)', 'col_name': 'res'},
    {'expression': "rpad(domain, 30, '#')", 'col_name': 'res'},
    {'expression': 'rtrim(domain)', 'col_name': 'res'},
    {'expression': "split(domain, '[a]', 2)", 'col_name': 'res'},
    {'expression': 'substring(domain, 1, 2)', 'col_name': 'res'},
    {'expression': 'trim(registrar)', 'col_name': 'res'},
    {'expression': 'upper(domain)', 'col_name': 'res'},
]

date_functions = [
    [
        {'expression': 'current_date()', 'col_name': 'date_col_1'},
        {'expression': 'current_timestamp()', 'col_name': 'date_col_2'},
        {'expression': 'unix_timestamp()', 'col_name': 'date_col_3'},
    ],
    {'expression': 'add_months(date_col_1, 10)', 'col_name': 'res'},
    {'expression': 'date_add(date_col_1, 10)', 'col_name': 'res'},
    {'expression': "date_format(date_col_1, 'MM/dd/yyy')", 'col_name': 'res'},
    {'expression': 'date_sub(date_col_1, 10)', 'col_name': 'res'},
    {'expression': "date_trunc('year', date_col_1)", 'col_name': 'res'},
    {'expression': 'date_diff(date_col_1, date_col_2)', 'col_name': 'res'},
    {'expression': 'dayofmonth(date_col_1)', 'col_name': 'res'},
    {'expression': 'dayofweek(date_col_1)', 'col_name': 'res'},
    {'expression': 'dayofyear(date_col_1)', 'col_name': 'res'},
    {'expression': "from_utc_timestamp(date_col_1, 'PST')", 'col_name': 'res'},
    {'expression': 'hour(date_col_1)', 'col_name': 'res'},
    {'expression': 'last_day(date_col_1)', 'col_name': 'res'},
    {'expression': 'minute(date_col_1)', 'col_name': 'res'},
    {'expression': 'month(date_col_1)', 'col_name': 'res'},
    {'expression': 'months_between(date_col_1, date_col_2)', 'col_name': 'res'},
    {'expression': 'quarter(date_col_1)', 'col_name': 'res'},
    {'expression': 'second(date_col_1)', 'col_name': 'res'},
    {'expression': 'to_unix_timestamp(created_at)', 'col_name': 'res'},
    {'expression': "to_utc_timestamp(created_at, 'JST')", 'col_name': 'res'},
    {'expression': 'weekofyear(date_col_1)', 'col_name': 'res'},
    {'expression': 'year(date_col_1)', 'col_name': 'res'},
]

array_functions = [
    {'expression': 'array(domain, registrar)', 'col_name': 'array_col'},
    {'expression': "array_contains(array_col, 'nasmo.se')", 'col_name': 'res'},
    {'expression': 'element_at(array_col, 1)', 'col_name': 'res'},
    {'expression': 'array_size(array_col)', 'col_name': 'res'},
    {'expression': "array_join(array_col, '---')", 'col_name': 'res'},
    {'expression': 'array_sort(array_col)', 'col_name': 'res'},
]

dummy_json = '{"f1": "value1", "f2": "value2"}'

misc_functions = [
    {'expression': 'coalesce(domain, registrar)', 'col_name': 'res'},
    {'expression': 'greatest(domain, registrar)', 'col_name': 'res'},
    {'expression': 'hash(domain)', 'col_name': 'res'},
    {'expression': 'isnull(domain)', 'col_name': 'res'},
    {'expression': 'least(domain, registrar)', 'col_name': 'res'},
    {'expression': 'md5(domain)', 'col_name': 'res'},
    {'expression': 'monotonically_increasing_id()', 'col_name': 'res'},
    {'expression': 'sha1(domain)', 'col_name': 'res'},
    # {'expression': "from_json(json_col, 'MAP<STRING,INT>')", 'col_name': 'res'},
]
