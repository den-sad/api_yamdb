from rest_framework import permissions


class isModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            if user.role == "moderator":
                return True
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = request.user
            if user.role == "moderator":
                return True
            return False


class isAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            if user.role == "admin":
                return True
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = request.user
            if user.role == "admin":
                return True
            return False


class isSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_staff
        return False


class NoPUT(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            return False
        return True
