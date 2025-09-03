from rest_framework.permissions import BasePermission


class AllowedToUpdateProfile(BasePermission):
    """Returns if a user is allowed to update a profile"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
