from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsReviewCreator, HasNoReviewForThisBusinessUser


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """
        Allows POSTing of a review only if the user is of type customer
        and has not reviewed the business_user already
        """
        if self.request.method == 'POST':
            return [IsCustomer(), HasNoReviewForThisBusinessUser()]
        return [IsAuthenticated()]


class ReviewUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewCreator]
