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


def notify_plan_change(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)

        for child_session in self.child_sessions:
            child_session.update_status.trigger("Plan changed, operation add/edit/remove applied")

        return res

    return wrapper
