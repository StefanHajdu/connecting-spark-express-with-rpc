# SESSION METHODS
from collections.abc import Iterator
from typing import Any

from core.rpc_client import RpcClient

rpc_client = RpcClient()


def submit_load_dataset_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Submit load dataset node."""
    return rpc_client.submit_load_dataset_node(request_data)


def submit_load_from_session_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit load from session node."""
    return rpc_client.submit_load_from_session_node(request_data)


def submit_filter_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit filter node."""
    return rpc_client.submit_filter_node(request_data)


def submit_new_column_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Submit new column node."""
    return rpc_client.submit_new_column_node(request_data)


def submit_join_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit join node."""
    return rpc_client.submit_join_node(request_data)


def submit_table_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit table node."""
    return rpc_client.submit_table_node(request_data)


def submit_histogram_node(request_data: dict[str, Any]) -> dict[str, Any]:
    """Submit histogram node."""
    return rpc_client.submit_histogram_node(request_data)


def toggle_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Toggle node."""
    return rpc_client.toggle_node(request_data)


def remove_node(request_data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Remove node."""
    return rpc_client.remove_node(request_data)


def preview_dataset(request_data: dict[str, Any]):
    """Preview dataset with streaming."""
    return rpc_client.preview_dataset(request_data)


def summarize_dataset(request_data: dict[str, Any]) -> dict[str, Any]:
    """Summarize dataset."""
    return rpc_client.summarize_dataset(request_data)
