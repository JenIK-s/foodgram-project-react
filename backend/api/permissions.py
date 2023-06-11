from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, _, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsAuthenticated(BasePermission):
    def has_permission(self, request, _):
        return request.user and request.user.is_authenticated
