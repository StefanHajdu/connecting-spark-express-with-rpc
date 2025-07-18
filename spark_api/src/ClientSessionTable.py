from exceptions import DuplicateSessionException


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
