import logging
from asyncio import run

from fastapi import APIRouter, Request

from .service import create_session, fetch_session_status, load_sessions

logger = logging.getLogger(__name__)

router = APIRouter(tags=['session'])


@router.post('/')
def fetch_create_session_base(request: Request):
    """Create a new session."""
    request_data = run(request.json())
    response = create_session(request_data)
    return response


@router.post('/create')
def fetch_create_session(request: Request):
    """Create a new session."""
    request_data = run(request.json())
    response = create_session(request_data)
    return response


@router.post('/status')
def fetch_session_status_route(request: Request):
    """Get session status."""
    request_data = run(request.json())
    response = fetch_session_status(request_data)
    return response


@router.get('/sessions')
def get_load_sessions():
    """Load all sessions."""
    yield from load_sessions()
