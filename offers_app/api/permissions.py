from rest_framework.permissions import BasePermission

class IsUserOfTypeBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'business'