# SESSION METHODS
from collections.abc import Iterator
from typing import Any

from core.rpc_client import RpcClient

rpc_client = RpcClient()


def load_sessions() -> Iterator[dict[str, Any]]:
    """Load all sessions."""
    return rpc_client.load_sessions()


def create_session(request_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new session."""
    return rpc_client.create_session(request_data)


def get_session_status(session_id: str) -> dict[str, Any]:
    """Get session status."""
    return rpc_client.get_session_status(session_id)
