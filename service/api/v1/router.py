"""Aggregate API router for version 1 endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from modules.direct.routes import router as direct_router
from modules.rpc.routes import router as rpc_router

router = APIRouter()
router.include_router(direct_router)
router.include_router(rpc_router)
