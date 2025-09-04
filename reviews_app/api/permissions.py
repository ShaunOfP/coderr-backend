from rest_framework.permissions import BasePermission

from reviews_app.models import Review


class IsCustomer(BasePermission):
    """This checks if a user is of type customer or not"""

    def has_permission(self, request, view):
        return request.user.type == 'customer'


class IsReviewCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if the authenticated user is also the creator of the review"""
        return request.user == obj.reviewer
