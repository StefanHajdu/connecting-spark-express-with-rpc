from collections.abc import Iterator
from typing import Any

import grpc
import sparkapi_pb2

from core.exceptions import ApplicationError
from core.rpc_client import RpcClient
from core.utils import MessageToDict

rpc_client = RpcClient()


def load_sessions() -> Iterator[dict[str, Any]]:
    """Load all sessions with streaming response."""
    try:
        request = sparkapi_pb2.Empty()
        for response in rpc_client.client.loadSessions(request):
            response: sparkapi_pb2.SessionResponse
            yield MessageToDict(response)
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def create_session(request_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new Spark session."""
    try:
        request = sparkapi_pb2.NewSessionRequest(**request_data)
        response: sparkapi_pb2.NewSessionResponse = rpc_client.client.createSession(request)
        return MessageToDict(response)
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e


def fetch_session_status(session_id: str) -> dict[str, Any]:
    """Get session status."""
    try:
        request = sparkapi_pb2.SessionStatusRequest(session_id=session_id)
        response: sparkapi_pb2.StatusResponse = rpc_client.client.getSessionStatus(request)
        return MessageToDict(response)
    except grpc.RpcError as e:
        raise ApplicationError(message=str(e), code=500) from e
