from functools import wraps


class PermissionDeniedError(RuntimeError):
    pass


def requires_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.context.has_permission(permission):
                raise PermissionDeniedError(
                    f"Permission denied. Required permission: {permission}"
                )
            return await func(self, *args, **kwargs)

        setattr(wrapper, "__required_permission__", permission)
        return wrapper

    return decorator
