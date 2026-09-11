from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class GlobalSettings:
    host: str
    port: int
    transport: str
    public_base_url: str
    public_path: str
    identity_mode: str
    log_level: str
    request_timeout_seconds: int
    max_results: int


@dataclass(frozen=True)
class TenantSettings:
    tenant_id: str
    name: str
    odoo_url: str
    odoo_database: str
    odoo_username: str
    odoo_api_key: str
    bootstrap_user_id: str
    bootstrap_user_role: str


def load_global_settings() -> GlobalSettings:
    public_base_url = os.getenv(
        "MCP_PUBLIC_BASE_URL",
        "https://mycompany.com",
    ).strip()

    if public_base_url and not public_base_url.startswith(
        ("http://", "https://")
    ):
        public_base_url = f"https://{public_base_url}"

    return GlobalSettings(
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(
            os.getenv(
                "PORT",
                os.getenv("MCP_PORT", "8000"),
            )
        ),
        transport=os.getenv("MCP_TRANSPORT", "streamable-http"),
        public_base_url=public_base_url,
        public_path=os.getenv("MCP_PUBLIC_PATH", "/mcp"),
        identity_mode=os.getenv("IDENTITY_MODE", "hybrid"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
        max_results=int(os.getenv("MAX_RESULTS", "50")),
    )


def load_project_registry() -> list[dict]:
    path = Path("config/projects.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)["projects"]


def load_tenant_config(tenant_id: str) -> dict:
    path = Path("app/tenants") / f"{tenant_id}.json"
    if not path.exists():
        raise ConfigurationError(f"Unknown tenant: {tenant_id}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_tenant_settings(tenant_id: str) -> TenantSettings:
    project = next(
        (p for p in load_project_registry() if p["tenant_id"] == tenant_id and p.get("enabled", True)),
        None,
    )
    if not project:
        raise ConfigurationError(f"Tenant is not registered/enabled: {tenant_id}")

    prefix = project["env_prefix"]

    def req(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ConfigurationError(f"Missing required environment variable: {name}")
        return value

    return TenantSettings(
        tenant_id=req(f"{prefix}_CLIENT_ID"),
        name=req(f"{prefix}_CLIENT_NAME"),
        odoo_url=req(f"{prefix}_ODOO_URL"),
        odoo_database=req(f"{prefix}_ODOO_DATABASE"),
        odoo_username=os.getenv(f"{prefix}_ODOO_USERNAME", ""),
        odoo_api_key=req(f"{prefix}_ODOO_API_KEY"),
        bootstrap_user_id=os.getenv(f"{prefix}_BOOTSTRAP_USER_ID", "bootstrap-admin"),
        bootstrap_user_role=os.getenv(f"{prefix}_BOOTSTRAP_USER_ROLE", "mcp_admin"),
    )
