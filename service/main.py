import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from api.v1.router import api_router
from core.exceptions import ApplicationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title='API', version='1.0.0')


class SPAStaticFiles(StaticFiles):
    """Serve frontend assets and fall back to index.html for SPA routes."""

    async def get_response(self, path, scope):  # type: ignore[override]
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            return await super().get_response('index.html', scope)
        return response


FRONTEND_DIST = Path(__file__).resolve().parent.parent / 'client_app' / 'build'
FRONTEND_INDEX = FRONTEND_DIST / 'index.html'


COMMON_ERROR = {'UNKNOWN_ERROR': {'code': 'UNKNOWN_ERROR', 'message': 'Unknown error', 'statusCode': 500}}


@app.exception_handler(ApplicationError)
async def application_error_handler(request: Request, exc: ApplicationError):
    """Handle ApplicationError exceptions."""
    return JSONResponse(status_code=exc.code, content=exc.to_response(include_stack=False))


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f'Unhandled exception: {exc}', exc_info=True)
    error = ApplicationError(
        message=str(exc) if str(exc) else COMMON_ERROR['UNKNOWN_ERROR']['message'],
        code=500,
    )
    return JSONResponse(status_code=500, content=error.to_response(include_stack=True))


logger.info('Starting API server')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include API routes
app.include_router(api_router)


if FRONTEND_INDEX.exists():
    logger.info(f'Serving frontend from {FRONTEND_DIST}')
    app.mount('/', SPAStaticFiles(directory=FRONTEND_DIST, html=True), name='frontend')
else:
    logger.warning('Frontend build directory not found. Run "npm run build" in client_app to generate static assets.')


if __name__ == '__main__':
    import uvicorn

    logger.info('Starting server on http://localhost:4444')
    uvicorn.run('main:app', host='localhost', port=4444, reload=False)
