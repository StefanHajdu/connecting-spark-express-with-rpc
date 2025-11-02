import logging

from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)

router = APIRouter(tags=['direct'])


@router.post('/placeholder')
async def placeholder(request: Request):
    """Placeholder for future implementation."""
    data = await request.json()
    logger.info(f'received data: {data}')
    return list(data.values())
