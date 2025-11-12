import json
import logging
from collections.abc import Iterable
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .service import (
    preview_dataset,
    remove_node,
    submit_add_column_node,
    submit_filter_node,
    submit_histogram_node,
    submit_join_node,
    submit_load_dataset_node,
    submit_load_from_session_node,
    submit_table_node,
    summarize_dataset,
    toggle_node,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=['node'])


def _json_stream(sync_iterator: Iterable[dict[str, Any]]) -> Iterable[str]:
    """Stream dict payloads as NDJSON."""
    for item in sync_iterator:
        yield json.dumps(item, separators=(',', ':'), ensure_ascii=False) + '\n'


@router.post('/submitLoadDatasetNode')
def submit_load_dataset_node_route(request_data: dict[str, Any]):
    """Submit load dataset node."""
    return StreamingResponse(_json_stream(submit_load_dataset_node(request_data)), media_type='application/x-ndjson')


@router.post('/submitLoadFromSessionNode')
def submit_load_from_session_node_route(request_data: dict[str, Any]):
    """Submit load from session node."""
    return submit_load_from_session_node(request_data)


@router.post('/submitFilterNode')
def submit_filter_node_route(request_data: dict[str, Any]):
    """Submit filter node."""
    return submit_filter_node(request_data)


@router.post('/submitAddColumnNode')
def submit_add_column_node_route(request_data: dict[str, Any]):
    """Submit add column node."""
    return StreamingResponse(
        _json_stream(submit_add_column_node(request_data)),
        media_type='application/x-ndjson',
    )


@router.post('/submitJoinNode')
def submit_join_node_route(request_data: dict[str, Any]):
    """Submit join node."""
    return submit_join_node(request_data)


@router.post('/submitTableNode')
def submit_table_node_route(request_data: dict[str, Any]):
    """Submit table node."""
    return submit_table_node(request_data)


@router.post('/submitHistogramNode')
def submit_histogram_node_route(request_data: dict[str, Any]):
    """Submit histogram node."""
    return submit_histogram_node(request_data)


@router.post('/removeNode')
def remove_node_route(request_data: dict[str, Any]):
    """Remove node."""
    return StreamingResponse(_json_stream(remove_node(request_data)), media_type='application/x-ndjson')


@router.post('/toggleNode')
def toggle_node_route(request_data: dict[str, Any]):
    """Toggle node."""
    return StreamingResponse(_json_stream(toggle_node(request_data)), media_type='application/x-ndjson')


@router.post('/summarize')
def summarize_route(request_data: dict[str, Any]):
    """Summarize dataset."""
    return summarize_dataset(request_data)


@router.post('/preview')
def preview_route(request_data: dict[str, Any]):
    """Preview dataset."""
    return StreamingResponse(preview_dataset(request_data), media_type='text/plain')
