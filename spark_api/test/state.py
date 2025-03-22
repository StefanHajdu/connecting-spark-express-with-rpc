import os

from spark_api.src.constants import PLAN_NODE_ROOT_ID

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestState:
    def __init__(self):
        self.path = (f'{CURRENT_DIR}/../../data/domains_small.csv',)
        self.type = 'csv'
        self.total_rows = 499_999
        self.root_node_id = PLAN_NODE_ROOT_ID
