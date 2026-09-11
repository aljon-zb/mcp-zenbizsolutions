from __future__ import annotations

from typing import Any
import requests


class OdooClient:
    def __init__(
        self,
        *,
        base_url: str,
        database: str,
        api_key: str,
        timeout_seconds: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.database = database
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Odoo-Database": self.database,
        }

    def search_read(
        self,
        model: str,
        domain: list,
        fields: list[str],
        *,
        limit: int = 50,
        offset: int = 0,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        payload = {
            "domain": domain,
            "fields": fields,
            "limit": limit,
            "offset": offset,
        }
        if order:
            payload["order"] = order

        response = requests.post(
            f"{self.base_url}/json/2/{model}/search_read",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()
