from rest_framework.permissions import BasePermission

from reviews_app.models import Review


class IsCustomer(BasePermission):
    """This checks if a user is of type customer or not and if hes authenticated."""

    def has_permission(self, request, view):
        return (request.user.type == 'customer'
                and request.user.is_authenticated)


class HasNoReviewForThisBusinessUser(BasePermission):
    message = 'You already have posted a review to this business user'

    def has_permission(self, request, view):
        """
        Checks if a business_user id is provided in the send data 
        and if the authenticated user has already posted a review for the provided business_user.
        """
        user = request.user
        business_user_id = request.data.get('business_user')

        if not business_user_id:
            return False

        already_reviewed = Review.objects.filter(
            business_user_id=business_user_id,
            reviewer=user
        ).exists()

        return not already_reviewed


class IsReviewCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if the authenticated user is also the creator of the review"""
        return request.user == obj.reviewer
