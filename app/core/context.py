from dataclasses import dataclass, field


@dataclass
class UserContext:
    user_id: str
    tenant_id: str
    role: str
    permissions: set[str] = field(default_factory=set)
    identity_mode: str = "individual"
    external_subject: str | None = None

    def has_permission(self, permission: str) -> bool:
        return "*" in self.permissions or permission in self.permissions
