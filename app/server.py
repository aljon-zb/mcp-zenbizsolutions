from __future__ import annotations

import logging
from contextvars import ContextVar

from mcp.server.fastmcp import FastMCP

from app.config import load_global_settings
from app.core.context import UserContext
from app.core.identity import resolve_bootstrap_context
from app.core.tenant_resolver import TenantRuntimeResolver
from app.tools.odoo.contacts import ContactsTools
from app.tools.odoo.sales import SalesTools
from app.tools.odoo.inventory import InventoryTools

settings = load_global_settings()
logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))

mcp = FastMCP(
    name="Company Multi-Tenant MCP",
    stateless_http=True,
    json_response=True,
)

tenant_resolver = TenantRuntimeResolver()

# In production this context should be populated by validated OAuth/SSO middleware
# for every request/session. For bootstrap testing, set a tenant before use.
current_user_context: ContextVar[UserContext | None] = ContextVar(
    "current_user_context",
    default=None,
)


def get_context() -> UserContext:
    context = current_user_context.get()
    if context is None:
        raise RuntimeError(
            "No authenticated MCP user context. "
            "OAuth/internal-login middleware must resolve the user and tenant."
        )
    return context


def build_tool_group(group_class):
    context = get_context()
    client = tenant_resolver.get_odoo_client(context.tenant_id)
    return group_class(client=client, context=context)


@mcp.tool()
async def contacts_list_contacts(search: str = "", limit: int = 20):
    return await build_tool_group(ContactsTools).list_contacts(search, limit)


@mcp.tool()
async def sales_list_sales_orders(limit: int = 20):
    return await build_tool_group(SalesTools).list_sales_orders(limit)


@mcp.tool()
async def inventory_search_products(search: str, limit: int = 20):
    return await build_tool_group(InventoryTools).search_products(search, limit)


@mcp.tool()
async def system_bootstrap_as_tenant(tenant_id: str):
    """
    DEVELOPMENT ONLY.

    Temporarily resolve the configured bootstrap user for PeltierPro or ZenBiz.
    Remove/disable this tool once OAuth/SSO is enabled.
    """
    context = resolve_bootstrap_context(tenant_id)
    current_user_context.set(context)

    return {
        "success": True,
        "tenant_id": context.tenant_id,
        "user_id": context.user_id,
        "role": context.role,
        "identity_mode": context.identity_mode,
    }


if __name__ == "__main__":
    # FastMCP 1.x does not accept host/port as arguments to run().
    # Configure them through mcp.settings instead.
    mcp.settings.host = settings.host
    mcp.settings.port = settings.port

    mcp.run(
        transport=settings.transport
    )
