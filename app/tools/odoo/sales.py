from app.core.permissions import requires_permission
from app.tools.base import BaseToolGroup


class SalesTools(BaseToolGroup):
    namespace = "sales"

    @requires_permission("sales.read")
    async def list_sales_orders(self, limit: int = 20):
        return self.client.search_read(
            "sale.order",
            [],
            ["id", "name", "partner_id", "state", "amount_total", "date_order"],
            limit=limit,
            order="date_order desc",
        )
