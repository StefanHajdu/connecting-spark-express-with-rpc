import json
import logging

from fastapi import APIRouter, Request
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from fastapi.responses import StreamingResponse

from .service import create_session, fetch_session_status, load_sessions

logger = logging.getLogger(__name__)

router = APIRouter(tags=['session'])


async def _async_json_stream(sync_iterator):
    """Stream dict payloads as NDJSON without blocking the event loop."""
    async for item in iterate_in_threadpool(sync_iterator):
        yield json.dumps(item, separators=(',', ':'), ensure_ascii=False) + '\n'


@router.post('/')
async def fetch_create_session_base(request: Request):
    """Create a new session."""
    request_data = await request.json()
    response = await run_in_threadpool(create_session, request_data)
    return response


@router.post('/create')
async def fetch_create_session(request: Request):
    """Create a new session."""
    request_data = await request.json()
    response = await run_in_threadpool(create_session, request_data)
    return response


@router.post('/status')
async def fetch_session_status_route(request: Request):
    """Get session status."""
    request_data = await request.json()
    response = await run_in_threadpool(fetch_session_status, request_data)
    return response


@router.get('/sessions')
async def get_load_sessions():
    """Load all sessions."""
    return StreamingResponse(
        _async_json_stream(load_sessions()),
        media_type='application/x-ndjson',
    )
