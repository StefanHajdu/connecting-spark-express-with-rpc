import os

from spark_api.src.constants import PLAN_NODE_ROOT_ID

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestState:
    def __init__(self):
        self.path = (f'{CURRENT_DIR}/../../data/domains_small.csv',)
        self.type = 'csv'
        self.total_rows = 499_999
        self.root_node_id = PLAN_NODE_ROOT_ID


text_filters = [
    {
        'case': {
            'expressions_json': ["contains(domain, 'club')"],
            'matching': '',
        },
        'correct': 2475,
    },
    {
        'case': {
            'expressions_json': ["ilike(registrar, 'G_Daddy.com, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {
        'case': {
            'expressions_json': ["ilike(registrar, 'GoDaddy.com, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {
        'case': {
            'expressions_json': ["ilike(registrar, 'GoDaddy.%, LLC')"],
            'matching': '',
        },
        'correct': 85127,
    },
    {
        'case': {
            'expressions_json': ["ilike(registrar, '成%维数码科技有限公司')"],
            'matching': '',
        },
        'correct': 340,
    },
    {
        'case': {
            'expressions_json': ["rlike(domain, '(https?:\/\/)?(www\.)?[a-z0-9-]+\.(com|org)(\.[a-z]{{2,3}})?')"],
            'matching': '',
        },
        'correct': 301352,
    },
    {
        'case': {
            'expressions_json': ["startswith(registrar, 'GoDaddy')"],
            'matching': '',
        },
        'correct': 93668,
    },
    {
        'case': {
            'expressions_json': ["endswith(registrar, 'com')"],
            'matching': '',
        },
        'correct': 19551,
    },
]
