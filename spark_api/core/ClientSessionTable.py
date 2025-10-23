from __future__ import annotations

from core import Client
from core.exceptions import DuplicateSessionException


class ClientSessionTable:
    def __init__(self):
        self.session_table: dict[str, Client.ClientSession] = {}

    def add(self, session_id: str, session: Client.ClientSession):
        print(f'/createSession: {session_id}')
        if session_id in self.session_table:
            raise DuplicateSessionException()
        else:
            self.session_table.update({session_id: session})

    def get_session(self, session_id: str) -> Client.ClientSession:
        return self.session_table[session_id]
