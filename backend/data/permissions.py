from rest_framework import permissions


class UserIsOwnerOrAdmin(permissions.BasePermission):
    @staticmethod
    def has_permission(request, view):
        return request.user and request.user.is_authenticated()

    @staticmethod
    def check_object_permission(user, obj):
        return user and user.is_authenticated() and (user.is_staff or obj == user)

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)
