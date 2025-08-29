from rest_framework.permissions import BasePermission


class IsOfTypeCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'customer'


class IsOfTypeBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'business'
