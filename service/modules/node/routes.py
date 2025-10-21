import logging

from fastapi import APIRouter, Request

from .service import (
    preview_dataset,
    remove_node,
    submit_filter_node,
    submit_histogram_node,
    submit_join_node,
    submit_load_dataset_node,
    submit_load_from_session_node,
    submit_new_column_node,
    submit_table_node,
    summarize_dataset,
    toggle_node,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=['node'])


@router.post('/submitLoadDatasetNode')
async def submit_load_dataset_node_route(request: Request):
    """Submit load dataset node."""
    request_data = await request.json()
    response = submit_load_dataset_node(request_data)
    return response


@router.post('/submitLoadFromSessionNode')
async def submit_load_from_session_node_route(request: Request):
    """Submit load from session node."""
    request_data = await request.json()
    response = submit_load_from_session_node(request_data)
    return response


@router.post('/submitFilterNode')
async def submit_filter_node_route(request: Request):
    """Submit filter node."""
    request_data = await request.json()
    response = submit_filter_node(request_data)
    return response


@router.post('/submitAddColumnNode')
async def submit_new_column_node_route(request: Request):
    """Submit new column node."""
    request_data = await request.json()
    response = submit_new_column_node(request_data)
    return response


@router.post('/submitJoinNode')
async def submit_join_node_route(request: Request):
    """Submit join node."""
    request_data = await request.json()
    response = submit_join_node(request_data)
    return response


@router.post('/submitTableNode')
async def submit_table_node_route(request: Request):
    """Submit table node."""
    request_data = await request.json()
    response = submit_table_node(request_data)
    return response


@router.post('/submitHistogramNode')
async def submit_histogram_node_route(request: Request):
    """Submit histogram node."""
    request_data = await request.json()
    response = submit_histogram_node(request_data)
    return response


@router.post('/removeNode')
async def remove_node_route(request: Request):
    """Remove node."""
    request_data = await request.json()
    response = remove_node(request_data)
    return response


@router.post('/toggleNode')
async def toggle_node_route(request: Request):
    """Toggle node."""
    request_data = await request.json()
    response = toggle_node(request_data)
    return response


@router.post('/summarize')
async def summarize_route(request: Request):
    """Summarize dataset."""
    request_data = await request.json()
    response = summarize_dataset(request_data)
    return response


@router.post('/preview')
async def preview_route(request: Request):
    """Preview dataset."""
    request_data = await request.json()
    response = preview_dataset(request_data)
    return response
