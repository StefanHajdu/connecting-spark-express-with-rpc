import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestState:
    __test__ = False

    def __init__(self):
        self.path = f'{CURRENT_DIR}/../../data/domains_small.parquet'
        self.type = 'parquet'
        self.total_rows = 499_999
        self.root_node_id = '0000-0000-0000'
