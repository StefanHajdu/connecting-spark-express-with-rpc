from custom_exceptions import DuplicateSessionException


class ClientSessionTable:
    def __init__(self):
        self.session_table = {}

    def add(self, id, session):
        print(f'/createSession: {id}')
        if id in self.session_table:
            raise DuplicateSessionException()
        else:
            self.session_table.update({id: session})

    def get_session(self, session_id: str):
        return self.session_table[session_id]


class SessionPlannerMap:
    def __init__(self, table):
        self.session_planners = {}
        self.session_table = table

    def add_session(self, session_id: str):
        self.session_planners.update({session_id: None})

    def get_session_plan(self, session_id: str):
        return self.session_planners[session_id]

    def update_session_plan(self, session_id: str, plan):
        self.session_planners[session_id] = plan
