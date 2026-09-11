# Unified Multi-Tenant MCP

This project implements the architecture where **all tenants use one public MCP endpoint**:

```text
https://mycompany.com/mcp
```

There is no public tenant-specific MCP URL such as:

```text
/mycompany.com/peltierpro/mcp
/mycompany.com/zenbiz/mcp
```

Instead, the authenticated user/session resolves:

```text
user -> tenant -> role -> permissions -> tenant integration
```

## Existing tenants

- PeltierPro
- ZenBiz

## Why the per-project public URLs were removed

The previous `PELTIERPRO_PUBLIC_URL` and `ZENBIZ_PUBLIC_URL` values are redundant in a single-gateway architecture.

Only one global public MCP endpoint is required:

```env
MCP_PUBLIC_BASE_URL=https://mycompany.com
MCP_PUBLIC_PATH=/mcp
```

However, these are **not redundant** and remain tenant-specific:

```env
PELTIERPRO_ODOO_URL=...
PELTIERPRO_ODOO_DATABASE=...
PELTIERPRO_ODOO_API_KEY=...

ZENBIZ_ODOO_URL=...
ZENBIZ_ODOO_DATABASE=...
ZENBIZ_ODOO_API_KEY=...
```

Those values point to different backend systems/credentials.

## Identity modes

The project is prepared for:

```text
shared
individual
hybrid
```

`hybrid` is recommended while migrating from one shared AI account to individual Business/Enterprise seats.

### Shared account

```text
Shared Claude/ChatGPT account
        |
        v
Your internal employee login
        |
        v
Internal user
        |
        v
Tenant + role + permissions
```

### Individual seat

```text
Employee's Claude/ChatGPT seat
        |
        v
OAuth / SSO identity
        |
        v
Internal user mapping
        |
        v
Tenant + role + permissions
```

## Current bootstrap mode

OAuth is disabled in the provided `.env`.

For development only, the project contains:

```text
system_bootstrap_as_tenant
```

so you can select `peltierpro` or `zenbiz` and test tenant routing.

Remove/disable this tool when real OAuth/SSO middleware is implemented.

## Next production step

Replace bootstrap context with validated OAuth/SSO claims such as:

```json
{
  "sub": "user_123",
  "tenant_id": "peltierpro",
  "role": "sales_manager",
  "identity_mode": "individual"
}
```

For a shared AI account, your own internal login can issue equivalent claims after the employee signs in.

## Security note

The generated `.env` contains credentials supplied for this project and is excluded by `.gitignore`.

Do not commit `.env` to a Git repository.
# mcp-zenbizsolutions


## Railway runtime compatibility

This project is pinned to MCP Python SDK 1.x with `mcp>=1.12.0,<2`.
FastMCP 1.x requires host and port to be assigned through `mcp.settings` before calling `run()`. Railway's injected `PORT` variable is preferred automatically, with `MCP_PORT` as the local fallback. `MCP_PUBLIC_BASE_URL` is also normalized to HTTPS when entered without a scheme.
