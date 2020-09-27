from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    message = "You`re authenticated. Please log out and try again."

    def has_permission(self, request, view):
        return not request.user.is_authenticated
