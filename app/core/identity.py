from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.config import load_global_settings, load_tenant_config, load_tenant_settings
from app.core.context import UserContext


@dataclass
class IdentityClaims:
    subject: str
    tenant_id: str
    role: str
    identity_mode: str
    provider: str | None = None
    email: str | None = None


def permissions_for_role(tenant_id: str, role: str) -> set[str]:
    tenant = load_tenant_config(tenant_id)
    return set(tenant.get("roles", {}).get(role, []))


def resolve_context_from_claims(claims: dict[str, Any]) -> UserContext:
    """
    Future OAuth/SSO path.

    Expected claims after validation:
      sub
      tenant_id
      role
      identity_mode  (individual/shared/sso/service)
    """
    tenant_id = str(claims["tenant_id"])
    role = str(claims["role"])

    return UserContext(
        user_id=str(claims["sub"]),
        tenant_id=tenant_id,
        role=role,
        permissions=permissions_for_role(tenant_id, role),
        identity_mode=str(claims.get("identity_mode", "individual")),
        external_subject=str(claims.get("sub")),
    )


def resolve_bootstrap_context(tenant_id: str) -> UserContext:
    """
    Temporary no-database/no-OAuth path.
    Useful while AUTH_ENABLED=false.
    """
    settings = load_tenant_settings(tenant_id)

    return UserContext(
        user_id=settings.bootstrap_user_id,
        tenant_id=tenant_id,
        role=settings.bootstrap_user_role,
        permissions=permissions_for_role(tenant_id, settings.bootstrap_user_role),
        identity_mode=load_global_settings().identity_mode,
    )
