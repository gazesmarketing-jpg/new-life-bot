"""FastAPI dependencies: get current user, role checks."""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select

from app.config import settings
from app.models.user import User

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> User:
    """Decode the token and look up the staff user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    role = payload.get("role")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
        )
    # In a full build this queries the DB
    from app import database
    async for session in database.get_async_session():
        # Simplified lookup for demo; full build uses a repository
        from app.models import User as UserModel
        stmt = select(UserModel).where(UserModel.id == int(user_id))
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )
        return user
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database unavailable",
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("iss") != settings.secret_key:
            return {}
        return payload
    except JWTError:
        return {}


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Require an admin role for sensitive endpoints."""
    from app.core.permissions import Role
    if user.role != Role.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


async def get_current_roles(
    required_roles: list,
    user: User = Depends(get_current_user),
) -> User:
    from app.core.permissions import Role
    allowed = {Role(r).value for r in required_roles}
    if user.role not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user


from app.core.permissions import Role, is_admin, has_permission

__all__ = [
    "get_current_user",
    "get_current_admin",
    "get_current_roles",
    "Role",
    "is_admin",
    "has_permission",
]

__all__ = [
    "get_current_user",
    "get_current_admin",
    "get_current_roles",
    "Role",
    "is_admin",
    "has_permission",
]
