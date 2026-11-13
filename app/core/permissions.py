"""Role and permission definitions for the staff dashboard."""

from __future__ import annotations

from enum import Enum
from typing import FrozenSet, Set


class Role(str, Enum):
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    REGISTRATION_OFFICER = "registration_officer"
    FINANCE_OFFICER = "finance_officer"


# Permission definitions per role (the actions each role can perform)
RolePermissions = {
    Role.ADMIN: {
        "staff:create",
        "staff:read",
        "staff:edit",
        "staff:deactivate",
        "program:manage",
        "registration:manage",
        "registration:approve",
        "registration:reject",
        "class:manage",
        "class:assign",
        "payment:manage",
        "document:manage",
        "notification:manage",
        "report:manage",
        "audit:read",
        "dashboard:read",
    },
    Role.RECEPTIONIST: {
        "staff:read",
        "program:read",
        "registration:view",
        "registration:edit",
        "registration:contact",
        "registration:note",
        "registration:submit",
        "student:read",
        "document:view",
        "document:manage",
        "class:manage",
        "class:view",
        "class:assign",
        "report:view",
        "dashboard:read",
    },
    Role.REGISTRATION_OFFICER: {
        "program:read",
        "registration:view",
        "registration:approve",
        "registration:reject",
        "registration:edit",
        "registration:contact",
        "student:read",
        "class:manage",
        "class:view",
        "class:assign",
        "report:view",
        "dashboard:read",
    },
    Role.FINANCE_OFFICER: {
        "program:read",
        "registration:view",
        "payment:view",
        "payment:edit",
        "payment:reminder",
        "report:view",
        "dashboard:read",
    },
}


# Actions that always require admin
ADMIN_ONLY_ACTIONS = {
    "staff:create",
    "staff:deactivate",
    "staff:edit:role",
    "program:manage",
    "notification:manage",
}


def has_permission(role: Role, action: str) -> bool:
    """Return True if *role* may perform *action*."""
    return action in RolePermissions.get(role, set())


def is_admin(role: Role) -> bool:
    """Return True if *role* is an administrator."""
    return role == Role.ADMIN


def is_authorized(role: Role, action: str, admin_only: bool = False) -> bool:
    """Check whether *role* may perform *action*."""
    if admin_only and not is_admin(role):
        return False
    return has_permission(role, action)
