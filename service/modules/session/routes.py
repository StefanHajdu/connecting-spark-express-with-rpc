import logging

from fastapi import APIRouter, Request

from .service import create_session, get_session_status, load_sessions

logger = logging.getLogger(__name__)

router = APIRouter(tags=['session'])


@router.post('/')
async def session_route(request: Request):
    """Create a new session."""
    request_data = await request.json()
    response = create_session(request_data)
    return response


@router.post('/create')
async def create_session_route(request: Request):
    """Create a new session."""
    request_data = await request.json()
    response = create_session(request_data)
    return response


@router.post('/status')
async def get_session_status_route(request: Request):
    """Get session status."""
    request_data = await request.json()
    response = get_session_status(request_data)
    return response


@router.get('/sessions')
def load_sessions_route():
    """Load all sessions."""
    sessions = []
    for session in load_sessions():
        sessions.append(session)
    return sessions
