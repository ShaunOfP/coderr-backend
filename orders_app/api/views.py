from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from orders_app.models import Order
from .serializers import OrderCreateSerializer, OrderResponseSerializer
from .permissions import IsOfTypeCustomer


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()

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
    pass


class OrderCountDetailView(RetrieveAPIView):
    pass


class OrderCompleteCountView(RetrieveAPIView):
    pass
