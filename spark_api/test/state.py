from spark_api.src.constants import PLAN_NODE_ROOT_ID


class TestState:
    def __init__(self):
        self.path = ("/home/stephenx/Documents/Datasets/domains_sub_test.csv",)
        self.type = "csv"
        self.total_rows = 499_999
        self.root_node_id = PLAN_NODE_ROOT_ID
