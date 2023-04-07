from rest_framework import permissions


class GetUpdateOwnProfile(permissions.BasePermission):
    """Allow the users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to get/edit their own profile"""
        if request.method in ("GET", "PUT", "DELETE"):
            return obj.id == request.user.id
