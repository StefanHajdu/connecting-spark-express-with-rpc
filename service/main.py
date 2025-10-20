"""Entry point for the FastAPI service."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import router as api_router
from core.error_handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title='Spark RPC Bridge')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(api_router)
    register_exception_handlers(app)

    @app.on_event('shutdown')
    async def _shutdown() -> None:
        client = get_rpc_client()
        client.close()
        if hasattr(get_rpc_client, 'cache_clear'):
            get_rpc_client.cache_clear()

    return app


app = create_app()
