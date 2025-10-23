from collections.abc import Iterator
from typing import Any

import grpc
import sparkapi_pb2

from core.exceptions import ApplicationError
from core.rpc_client import RpcClient

rpc_client = RpcClient()


def load_sessions() -> Iterator[dict[str, Any]]:
    """Load all sessions with streaming response."""
    try:
        request = sparkapi_pb2.Empty()
        for response in rpc_client.client.loadSessions(request):
            response: sparkapi_pb2.SessionResponse
            print('Loaded session:', response)
            yield {
                'session_id': response.session_id,
                'name': response.name,
                'nodes': [
                    {
                        'session_id': node.session_id,
                        'node_id': node.node_id,
                        'prev_node_id': node.prev_node_id,
                        'invalid_state': {
                            'active': node.invalid_state.active,
                            'error_msg': node.invalid_state.error_msg,
                        },
                        'active': node.active,
                        'columns': [{'name': col.name, 'dtype': col.dtype} for col in node.columns],
                        'title': node.title,
                        'user_input': node.user_input,
                    }
                    for node in response.nodes
                ],
            }
    except grpc.RpcError as e:
        print('gRPC error while loading sessions:', e)
        raise ApplicationError(message=str(e), code=500) from e


def create_session(request_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new Spark session."""
    try:
        request = sparkapi_pb2.NewSessionRequest(**request_data)
        response: sparkapi_pb2.NewSessionResponse = rpc_client.client.createSession(request)
        return {'session_id': response.session_id, 'name': response.msg}
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise ApplicationError(message='Session already exists.', code=400) from e
        raise ApplicationError(message=str(e), code=500) from e


def fetch_session_status(session_id: str) -> dict[str, Any]:
    """Get session status."""
    try:
        request = sparkapi_pb2.SessionStatusRequest(session_id=session_id)
        response: sparkapi_pb2.StatusResponse = rpc_client.client.getSessionStatus(request)
        return {'session_id': response.session_id, 'rebuild_recommendation': response.rebuild_recommendation, 'cause': response.cause}
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e
