from rest_framework.permissions import BasePermission


class IsOfTypeCustomer(BasePermission):
    """Returns a boolean based on if the currently authenticated user is of type customer"""

    def has_permission(self, request, view):
        return request.user.type == 'customer'


class IsOfTypeBusiness(BasePermission):
    """Returns a boolean based on if the currently authenticated user is of type business"""

    def has_permission(self, request, view):
        return request.user.type == 'business'
