from app.core.permissions import requires_permission
from app.tools.base import BaseToolGroup


class ContactsTools(BaseToolGroup):
    namespace = "contacts"

    @requires_permission("contacts.read")
    async def list_contacts(self, search: str = "", limit: int = 20):
        domain = [["type", "=", "contact"]]
        if search:
            domain.extend(["|", ["name", "ilike", search], ["email", "ilike", search]])

        return self.client.search_read(
            "res.partner",
            domain,
            ["id", "name", "email", "phone", "mobile", "is_company"],
            limit=limit,
            order="name asc",
        )
