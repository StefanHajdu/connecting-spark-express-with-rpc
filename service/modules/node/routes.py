import json
import logging
from asyncio import run
from collections.abc import Iterator
from typing import Any

from fastapi import APIRouter, Request
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


def json_stream_response(generator: Iterator[Any], media_type: str = 'application/json') -> StreamingResponse:
    """Helper to convert a dict generator to a JSON streaming response."""

    def generate():
        for item in generator:
            yield json.dumps(item) + '\n'

    return StreamingResponse(generate(), media_type=media_type)


@router.post('/submitLoadDatasetNode')
def submit_load_dataset_node_route(request: Request):
    """Submit load dataset node."""
    request_data = run(request.json())
    return list(submit_load_dataset_node(request_data))


@router.post('/submitLoadFromSessionNode')
def submit_load_from_session_node_route(request: Request):
    """Submit load from session node."""
    request_data = run(request.json())
    response = submit_load_from_session_node(request_data)
    return response


@router.post('/submitFilterNode')
def submit_filter_node_route(request: Request):
    """Submit filter node."""
    request_data = run(request.json())
    response = submit_filter_node(request_data)
    return response


@router.post('/submitAddColumnNode')
def submit_add_column_node_route(request: Request):
    """Submit add column node."""
    request_data = run(request.json())
    return list(submit_add_column_node(request_data))


@router.post('/submitJoinNode')
def submit_join_node_route(request: Request):
    """Submit join node."""
    request_data = run(request.json())
    response = submit_join_node(request_data)
    return response


@router.post('/submitTableNode')
def submit_table_node_route(request: Request):
    """Submit table node."""
    request_data = run(request.json())
    response = submit_table_node(request_data)
    return response


@router.post('/submitHistogramNode')
def submit_histogram_node_route(request: Request):
    """Submit histogram node."""
    request_data = run(request.json())
    response = submit_histogram_node(request_data)
    return response


@router.post('/removeNode')
def remove_node_route(request: Request):
    """Remove node."""
    request_data = run(request.json())
    return list(remove_node(request_data))


@router.post('/toggleNode')
def toggle_node_route(request: Request):
    """Toggle node."""
    request_data = run(request.json())
    return list(toggle_node(request_data))


@router.post('/summarize')
def summarize_route(request: Request):
    """Summarize dataset."""
    request_data = run(request.json())
    response = summarize_dataset(request_data)
    return response


@router.post('/preview')
def preview_route(request: Request):
    """Preview dataset."""
    request_data = run(request.json())
    return json_stream_response(preview_dataset(request_data), media_type='text/plain')
