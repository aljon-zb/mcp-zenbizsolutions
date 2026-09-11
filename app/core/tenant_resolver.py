from app.clients.odoo import OdooClient
from app.config import load_global_settings, load_tenant_settings


class TenantRuntimeResolver:
    def __init__(self):
        self._clients = {}

    def get_odoo_client(self, tenant_id: str) -> OdooClient:
        if tenant_id not in self._clients:
            settings = load_tenant_settings(tenant_id)
            global_settings = load_global_settings()

            self._clients[tenant_id] = OdooClient(
                base_url=settings.odoo_url,
                database=settings.odoo_database,
                api_key=settings.odoo_api_key,
                timeout_seconds=global_settings.request_timeout_seconds,
            )

        return self._clients[tenant_id]
