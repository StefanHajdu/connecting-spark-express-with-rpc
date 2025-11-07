import json
import logging

from fastapi import APIRouter, Request
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
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


async def async_json_stream(sync_iterator):
    """Async generator that wraps a synchronous iterator for streaming JSON without blocking the event loop."""
    async for item in iterate_in_threadpool(sync_iterator):
        yield json.dumps(item, separators=(',', ':'), ensure_ascii=False) + '\n'


@router.post('/submitLoadDatasetNode')
async def submit_load_dataset_node_route(request: Request):
    """Submit load dataset node."""
    request_data = await request.json()
    return StreamingResponse(async_json_stream(submit_load_dataset_node(request_data)), media_type='application/x-ndjson')


@router.post('/submitLoadFromSessionNode')
async def submit_load_from_session_node_route(request: Request):
    """Submit load from session node."""
    request_data = await request.json()
    response = await run_in_threadpool(submit_load_from_session_node, request_data)
    return response


@router.post('/submitFilterNode')
async def submit_filter_node_route(request: Request):
    """Submit filter node."""
    request_data = await request.json()
    response = await run_in_threadpool(submit_filter_node, request_data)
    return response


@router.post('/submitAddColumnNode')
async def submit_add_column_node_route(request: Request):
    """Submit add column node."""
    request_data = await request.json()
    return StreamingResponse(
        async_json_stream(submit_add_column_node(request_data)),
        media_type='application/x-ndjson',  # More accurate media type for newline-delimited JSON
    )


@router.post('/submitJoinNode')
async def submit_join_node_route(request: Request):
    """Submit join node."""
    request_data = await request.json()
    response = await run_in_threadpool(submit_join_node, request_data)
    return response


@router.post('/submitTableNode')
async def submit_table_node_route(request: Request):
    """Submit table node."""
    request_data = await request.json()
    response = await run_in_threadpool(submit_table_node, request_data)
    return response


@router.post('/submitHistogramNode')
async def submit_histogram_node_route(request: Request):
    """Submit histogram node."""
    request_data = await request.json()
    response = await run_in_threadpool(submit_histogram_node, request_data)
    return response


@router.post('/removeNode')
async def remove_node_route(request: Request):
    """Remove node."""
    request_data = await request.json()
    return StreamingResponse(async_json_stream(remove_node(request_data)), media_type='application/x-ndjson')


@router.post('/toggleNode')
async def toggle_node_route(request: Request):
    """Toggle node."""
    request_data = await request.json()
    return StreamingResponse(async_json_stream(toggle_node(request_data)), media_type='application/x-ndjson')


@router.post('/summarize')
async def summarize_route(request: Request):
    """Summarize dataset."""
    request_data = await request.json()
    response = await run_in_threadpool(summarize_dataset, request_data)
    return response


@router.post('/preview')
async def preview_route(request: Request):
    """Preview dataset."""
    request_data = await request.json()
    return StreamingResponse(iterate_in_threadpool(preview_dataset(request_data)), media_type='text/plain')
