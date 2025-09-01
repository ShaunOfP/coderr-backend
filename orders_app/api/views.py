from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

from orders_app.models import Order
from .serializers import OrderCreateSerializer, OrderResponseSerializer, OrderCountSerializer, CompletedOrderCountSerializer
from .permissions import IsOfTypeCustomer, IsOfTypeBusiness
from userauth_app.models import CustomUser


class OrderListCreateView(ListCreateAPIView):
    def get_queryset(self):
        return Order.objects.filter(Q(business_user=self.request.user) | Q(customer_user=self.request.user))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderResponseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOfTypeCustomer()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        create_serializer = OrderCreateSerializer(
            data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        order = create_serializer.save()

        response_serializer = OrderResponseSerializer(
            order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderResponseSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), IsOfTypeBusiness()]


class OrderCountView(RetrieveAPIView):
    serializer_class = OrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business_pk = self.kwargs.get('pk')
        return CustomUser.objects.filter(pk=business_pk, type='business')


class OrderCompleteCountView(RetrieveAPIView):
    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business_pk = self.kwargs.get('pk')
        return CustomUser.objects.filter(pk=business_pk, type='business')
