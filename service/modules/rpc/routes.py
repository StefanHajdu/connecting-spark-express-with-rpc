"""API routes bridging HTTP requests to the Spark RPC service."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Annotated, Any, TypeAlias

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from core.exceptions import ApplicationError

JsonPayload: TypeAlias = Annotated[dict[str, Any] | None, Body(default=None)]

router = APIRouter(prefix='/rpc', tags=['rpc'])


def _json_array_stream(items: Iterator[dict[str, Any]]) -> Iterator[bytes]:
    iterator = iter(items)
    try:
        first_item = next(iterator)
    except StopIteration:
        yield b'[]'
        return
    except ApplicationError:
        raise
    yield b'['
    yield json.dumps(first_item).encode('utf-8')
    for item in iterator:
        yield b',' + json.dumps(item).encode('utf-8')
    yield b']'


def _text_stream(chunks: Iterator[str]) -> Iterator[bytes]:
    for chunk in chunks:
        yield chunk.encode('utf-8')


@router.post('/session/create')
async def create_session(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.create_session(payload or {})


@router.post('/session')
async def create_session_alias(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.create_session(payload or {})


@router.post('/session/status')
async def get_session_status(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.get_session_status(payload or {})


@router.post('/session/rebuild')
async def rebuild_session(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.rebuild_session(payload or {})


@router.get('/load/sessions')
async def load_sessions(client: RpcClientDep) -> StreamingResponse:
    stream = _json_array_stream(client.load_sessions())
    return StreamingResponse(stream, media_type='application/json')


@router.post('/load/submitLoadDatasetNode')
async def submit_load_dataset_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _json_array_stream(client.submit_load_dataset_node(payload or {}))
    return StreamingResponse(stream, media_type='application/json')


@router.post('/load/submitLoadFromSessionNode')
async def submit_load_from_session_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_load_from_session_node(payload or {})


@router.post('/sessionNode/transform/submitLoadDatasetNode')
async def session_submit_load_dataset_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _json_array_stream(client.submit_load_dataset_node(payload or {}))
    return StreamingResponse(stream, media_type='application/json')


@router.post('/sessionNode/transform/submitLoadFromSessionNode')
async def session_submit_load_from_session_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_load_from_session_node(payload or {})


@router.post('/sessionNode/transform/submitFilterNode')
async def submit_filter_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_filter_node(payload or {})


@router.post('/sessionNode/transform/submitAddColumnNode')
async def submit_add_column_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _json_array_stream(client.submit_add_column_node(payload or {}))
    return StreamingResponse(stream, media_type='application/json')


@router.post('/sessionNode/transform/submitJoinNode')
async def submit_join_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_join_node(payload or {})


@router.post('/sessionNode/transform/submitTableNode')
async def submit_table_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_table_node(payload or {})


@router.post('/sessionNode/transform/submitHistogramNode')
async def submit_histogram_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.submit_histogram_node(payload or {})


@router.post('/sessionNode/transform/removeNode')
async def remove_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _json_array_stream(client.remove_node(payload or {}))
    return StreamingResponse(stream, media_type='application/json')


@router.post('/sessionNode/transform/toggleNode')
async def toggle_node(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _json_array_stream(client.toggle_node(payload or {}))
    return StreamingResponse(stream, media_type='application/json')


@router.post('/sessionNode/action/summarize')
async def summarize_dataset(
    payload: JsonPayload,
    client: RpcClientDep,
) -> dict[str, Any]:
    return client.summarize_dataset(payload or {})


@router.post('/sessionNode/action/preview')
async def preview_dataset(
    payload: JsonPayload,
    client: RpcClientDep,
) -> StreamingResponse:
    stream = _text_stream(client.preview_dataset(payload or {}))
    return StreamingResponse(stream, media_type='application/json')
