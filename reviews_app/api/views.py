from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from reviews_app.models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsReviewCreator


class ReviewListCreateView(ListCreateAPIView):
    """
    This view allows the user to use the GET and POST-method.
    Filtering for business_user_id and reviewer_id are supported.
    Also supports ordering for updated_at and rating.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['updated_at', 'rating']

    def get_permissions(self):
        """
        Allows POSTing of a review only if the user is of type customer
        and has not reviewed the business_user already
        """
        if self.request.method == 'POST':
            return [IsCustomer()]
        return [IsAuthenticated()]


class ReviewUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    """This view allows for DELETE and PATCH/PUT calls"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewCreator]
