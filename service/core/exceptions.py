"""Custom exceptions used by the FastAPI service."""

from __future__ import annotations

import traceback
from typing import Any, Optional


class ApplicationError(Exception):
    """Represents an application-level error mapped to an HTTP response."""

    def __init__(
        self,
        *,
        message: str,
        code: int,
        errors: Optional[Any] = None,
        meta: Optional[Any] = None,
    ) -> None:
        if not message:
            raise ValueError('ApplicationError requires a message.')
        if not code:
            raise ValueError('ApplicationError requires a code.')
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors
        self.meta = meta
        self.stack = ''.join(traceback.format_stack())

    def to_response(self, include_stack: bool = False) -> dict[str, Any]:
        """Serialize the error into the HTTP payload structure."""
        payload: dict[str, Any] = {
            'code': self.code,
            'message': self.message,
        }
        if self.errors is not None:
            payload['errors'] = self.errors
        if self.meta is not None:
            payload['meta'] = self.meta
        if include_stack:
            payload['stack'] = self.stack
        return {'error': payload}
