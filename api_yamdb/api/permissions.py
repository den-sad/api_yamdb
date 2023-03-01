from rest_framework import permissions


class isModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == "moderator")

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == "moderator")


class isAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_authenticated
                    and request.user.role == "admin")


class isSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_staff


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin')
