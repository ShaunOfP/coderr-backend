from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework.response import Response

from offers_app.models import Offer
from userauth_app.models import CustomUser
from reviews_app.models import Review


class BaseInfoView(APIView):
    """The view for the base-info endpoint"""
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """Retrieves the given info points from the database when the endpoint is called and returns the info as a response"""
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']

        data = {
            'review_count': Review.objects.count(),
            'average_rating': f"{average_rating:.1f}" if average_rating is not None else 0,
            'business_profile_count': CustomUser.objects.filter(type='business').count(),
            'offer_count': Offer.objects.count()
        }
        return Response(data)
