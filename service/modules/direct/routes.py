"""Routes for direct interactions that do not use the gRPC backend."""

from __future__ import annotations

from pathlib import Path
from stat import S_ISDIR, S_ISREG

import anyio
from fastapi import APIRouter
from pydantic import BaseModel, Field

from core.exceptions import ApplicationError

router = APIRouter(prefix='/direct', tags=['direct'])


class ValidatePathRequest(BaseModel):
    path: str = Field(..., description='Absolute or relative filesystem path to validate.')


@router.post('/validatePath')
async def validate_path(payload: ValidatePathRequest) -> dict[str, bool | int]:
    """Validate that the provided path exists and return basic metadata."""
    raw_path = payload.path.strip()
    if not raw_path:
        raise ApplicationError(
            code='PATH_VALIDATION_ERROR',
            message='Request body must include a path to validate.',
            status_code=400,
        )

    path = Path(raw_path).expanduser()
    try:
        stats = await anyio.to_thread.run_sync(path.stat)
    except FileNotFoundError as exc:
        raise ApplicationError(
            code='PATH_VALIDATION_ERROR',
            message=f'Path validation error: {exc}',
            status_code=404,
        ) from exc
    except OSError as exc:
        raise ApplicationError(
            code='PATH_VALIDATION_ERROR',
            message=f'Path validation error: {exc}',
            status_code=400,
        ) from exc

    return {
        'is_file': S_ISREG(stats.st_mode),
        'is_dir': S_ISDIR(stats.st_mode),
        'size': stats.st_size,
    }
