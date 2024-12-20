from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пермишен с доступом на уровне объекта, с проверкой авторства."""

    def has_object_permission(self, request, view, obj):
        """Проверка на уровне объекта на безопасность запроса и авторство."""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user
