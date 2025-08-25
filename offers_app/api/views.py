from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from offers_app.models import Offer
from .serializers import OfferCreateSerializer, OfferGetSerializer
from .permissions import IsUserOfTypeBusiness
from .pagination import ResultSetPagination


class OfferListCreateView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['creator_id', 'min_price']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price']
    pagination_class = ResultSetPagination

    def get_queryset(self):
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
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferGetSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsUserOfTypeBusiness()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class OfferDeleteUpdateDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    # serializer_class =
    permission_classes = []


class OfferDetailsDetailView(RetrieveAPIView):
    queryset = Offer.objects.all()
    # serializer_class =
    permission_classes = []
