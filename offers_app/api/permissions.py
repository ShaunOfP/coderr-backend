from rest_framework.permissions import BasePermission

class IsUserOfTypeBusiness(BasePermission):
    """Returns True or False depending on the type of the authenticated user"""
    def has_permission(self, request, view):
        return request.user.type == 'business'
    

class IsOfferCreator(BasePermission):
    """Returns True if the authenticated user is the creator of the Offer. Returns False otherwise"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator