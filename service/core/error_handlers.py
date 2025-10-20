"""FastAPI exception handlers and registration helpers."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import ApplicationError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach custom exception handlers to the FastAPI application."""

    @app.exception_handler(ApplicationError)
    async def handle_application_error(request: Request, exc: ApplicationError) -> JSONResponse:
        content: dict[str, Any] = exc.to_response(include_stack=True)
        status_code = exc.status_code or 500
        return JSONResponse(status_code=status_code, content=content)

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception('Unhandled exception during request processing')
        app_error = ApplicationError(message=str(exc) or 'Unknown error', code='UNKNOWN_ERROR', status_code=500)
        content: dict[str, Any] = app_error.to_response(include_stack=True)
        return JSONResponse(status_code=500, content=content)
