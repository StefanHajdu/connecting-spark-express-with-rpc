import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title='API', version='1.0.0')


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


if __name__ == '__main__':
    import uvicorn

    logger.info('Starting server on http://0.0.0.0:4444')
    uvicorn.run('main:app', host='0.0.0.0', port=4444, reload=True)
