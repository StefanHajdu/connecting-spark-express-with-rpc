import datetime
from functools import wraps


def log_plan_execution(route: str):
    def inner_func(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start = datetime.datetime.now()
            print(f'\n>[start: {start}] PLAN TO APPLY for session: {self.id} <')
            res = func(self, *args, **kwargs)
            for idx, node in enumerate(self.plan.nodes):
                print(f'    {idx}. {node}')
            end = datetime.datetime.now()
            print(f'>[end: {end} | diff: {end - start}] PLAN EXECUTED for session: {self.id} <')
            print(f'{route} {args}')
            return res

        return wrapper

    return inner_func
