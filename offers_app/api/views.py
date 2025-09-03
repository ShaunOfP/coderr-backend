from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from offers_app.models import Offer, OfferDetail
from .serializers import OfferCreateSerializer, OfferGetSerializer, OfferSingleSerializer, OfferPatchSerializer, OfferDetailSerializer
from .permissions import IsUserOfTypeBusiness, IsOfferCreator
from .pagination import ResultSetPagination


class OfferListCreateView(ListCreateAPIView):
    """
    A customizable view to GET and POST Offers.
    """
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['creator_id', 'min_price']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price']
    pagination_class = ResultSetPagination

    def get_queryset(self):
        """
        If no filters are provided in the query params the normal queryset with all objects is returned.
        If filters are provided the queryset is filtered and returned with applied filters.
        """
        queryset = Offer.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(title__icontains=search_param,
                                       description__icontains=search_param)
        max_delivery_time_param = self.request.query_params.get(
            'max_delivery_time', None)
        if max_delivery_time_param is not None:
            queryset = queryset.filter(
                min_delivery_time__lte=max_delivery_time_param)
        return queryset

    def get_serializer_class(self):
        """Uses different serializers based on the request method"""
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferGetSerializer

    def get_permissions(self):
        """Checks for different permissions based on the request method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsUserOfTypeBusiness()]

    def perform_create(self, serializer):
        """When creating a new Offer the currently authenticated user is assigned as the creator automatically"""
        serializer.save(creator=self.request.user)


class OfferDeleteUpdateDetailView(RetrieveUpdateDestroyAPIView):
    """The view for the DELETE and PATCH-Method and to GET a single Offer"""
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        """Uses different serializers for different HTTP-Methods"""
        if self.request.method == 'GET':
            return OfferSingleSerializer
        return OfferPatchSerializer

    def get_permissions(self):
        """Uses different Permissions for different HTTP-Methods"""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOfferCreator()]


class OfferDetailsDetailView(RetrieveAPIView):
    """The view for the /api/offerdetails/{id}/ endpoint"""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
