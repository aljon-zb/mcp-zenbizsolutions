from app.core.permissions import requires_permission
from app.tools.base import BaseToolGroup


class InventoryTools(BaseToolGroup):
    namespace = "inventory"

    @requires_permission("inventory.read")
    async def search_products(self, search: str, limit: int = 20):
        return self.client.search_read(
            "product.product",
            ["|", ["name", "ilike", search], ["default_code", "ilike", search]],
            ["id", "name", "default_code", "qty_available", "virtual_available"],
            limit=limit,
            order="name asc",
        )
