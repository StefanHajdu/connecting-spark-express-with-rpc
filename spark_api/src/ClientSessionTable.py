from __future__ import annotations

from exceptions import DuplicateSessionException

import Client


class ClientSessionTable:
    def __init__(self):
        self.session_table: dict[str, Client.ClientSession] = {}

    def add(self, id: str, session: Client.ClientSession):
        print(f'/createSession: {id}')
        if id in self.session_table:
            raise DuplicateSessionException()
        else:
            self.session_table.update({id: session})

    def get_session(self, session_id: str) -> Client.ClientSession:
        return self.session_table[session_id]
