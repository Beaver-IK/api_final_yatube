from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пермишен с доступом на уровне объекта, с проверкой авторства."""

    def has_object_permission(self, request, view, obj):
        """Проверка на уровне объекта на безопасность запроса и авторство."""
        return bool(request.method in permissions.SAFE_METHODS
                    or obj.author == request.user)
