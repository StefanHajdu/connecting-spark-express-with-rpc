from fastapi import APIRouter

# from modules.direct import routes as direct_routes
from modules.node import routes as node_routes
from modules.session import routes as session_routes

api_router = APIRouter()

# api_router.include_router(direct_routes.router, prefix='/direct')
api_router.include_router(node_routes.router, prefix='/rpc/node')
api_router.include_router(session_routes.router, prefix='/rpc/session')
