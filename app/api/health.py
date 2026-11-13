"""Health and readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
async def health():
    """Basic service health check."""
    return {"status": "ok", "service": "new-life-dashboard", "database": "ok"}
