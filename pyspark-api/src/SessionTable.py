import grpc

import sparkapi_session_pb2_grpc


class DuplicateSessionException(Exception):
    def __init__(self, message="Duplicate sessions"):
        super().__init__(message)


class SessionTable:
    def __init__(self):
        self.session_table = {}

    def add(self, id, port):
        if id in self.session_table:
            raise DuplicateSessionException()
        else:
            channel = grpc.insecure_channel(f"localhost:{port}")
            stub = sparkapi_session_pb2_grpc.SparkApiSessionStub(channel)
            self.session_table.update({id: {"port": port, "channel": channel, "stub": stub}})

    def get_stub(self, session_id: str):
        return self.session_table[session_id]["stub"]
