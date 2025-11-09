import json
import logging
from collections.abc import Iterable
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .service import create_session, fetch_session_status, load_sessions

logger = logging.getLogger(__name__)

router = APIRouter(tags=['session'])


def _json_stream(sync_iterator: Iterable[dict[str, Any]]) -> Iterable[str]:
    """Stream dict payloads as NDJSON."""
    for item in sync_iterator:
        yield json.dumps(item, separators=(',', ':'), ensure_ascii=False) + '\n'


@router.post('/')
def fetch_create_session_base(request_data: dict[str, Any]):
    """Create a new session."""
    return create_session(request_data)


@router.post('/create')
def fetch_create_session(request_data: dict[str, Any]):
    """Create a new session."""
    return create_session(request_data)


@router.post('/status')
def fetch_session_status_route(request_data: dict[str, Any]):
    """Get session status."""
    return fetch_session_status(request_data)


@router.get('/sessions')
def get_load_sessions():
    """Load all sessions."""
    return StreamingResponse(
        _json_stream(load_sessions()),
        media_type='application/x-ndjson',
    )
