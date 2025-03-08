from functools import wraps


def log_plan_execution(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        print(f">>> PLAN TO APPLY for session: {self.id} >>>")
        for idx, node in enumerate(self.plan.nodes):
            print(f"    {idx}. {node}")
        print(f">>> PLAN TO APPLY for session: {self.id} >>>\n")
        return res

    return wrapper
