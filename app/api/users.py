"""Staff user account management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app import database
from app.core import security
from app.core.permissions import Role, is_admin
from app.models.user import User
from app.api.deps import get_current_admin, get_current_roles, decode_token

router = APIRouter(prefix="/users", tags=["staff"])


# ------------------------------------------------------------------ #
#  List / detail
# ------------------------------------------------------------------ #
@router.get("", response_model=List[User])
async def list_users(
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


@router.get("/{user_id}")
async def get_user(user_id: int, current_user = Depends(get_current_admin)):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


# ------------------------------------------------------------------ #
#  Create
# ------------------------------------------------------------------ #
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(payload: dict, current_user = Depends(get_current_admin)):
    """Create a new staff account. Requires an admin."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.username == payload.get("username"))
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")

        user = User(
            username=payload["username"],
            email=payload.get("email"),
            full_name=payload.get("full_name"),
            role=payload.get("role", "receptionist"),
            hashed_password=security.hash_password(payload["password"]),
            is_verified=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


# ------------------------------------------------------------------ #
#  Deactivate
# ------------------------------------------------------------------ #
@router.patch("/{user_id}/deactivate", response_model=User)
async def deactivate_user(
    user_id: int,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = False
        await session.commit()
        await session.refresh(user)
        return user
