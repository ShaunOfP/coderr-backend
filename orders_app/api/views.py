from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from orders_app.models import Order
from .serializers import OrderCreateSerializer, OrderResponseSerializer, OrderCountSerializer, CompletedOrderCountSerializer
from .permissions import IsOfTypeCustomer, IsOfTypeBusiness
from userauth_app.models import CustomUser


class OrderListCreateView(ListCreateAPIView):
    """The view for the endpoint /api/orders/ for the GET and POST-Method"""

    def get_queryset(self):
        """
        Returns the queryset with the orders connected to the authenticated user.
        The user can either be the offer creator or the order creator
        """
        return Order.objects.filter(Q(business_user=self.request.user) | Q(customer_user=self.request.user))

    def get_serializer_class(self):
        """Uses different serializers for different HTTP-Methods"""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderResponseSerializer

    def get_permissions(self):
        """Uses different permission for different HTTP-Methods"""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOfTypeCustomer()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Customizes the response when a new order is created"""
        create_serializer = OrderCreateSerializer(
            data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        order = create_serializer.save()

        response_serializer = OrderResponseSerializer(
            order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    """The view for the endpoint /api/orders/{id}/ for the PATCH and DELETE-Method"""
    queryset = Order.objects.all()
    serializer_class = OrderResponseSerializer

    def get_permissions(self):
        """Uses different permissions for different HTTP-Methods"""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), IsOfTypeBusiness()]


class OrderCountView(RetrieveAPIView):
    """The view for the endpoint /api/order-count/{business_user_id}/"""
    serializer_class = OrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the object with the provided id of the business user.
        If the user matching to the given id this returns a 404-error.
        """
        business_pk = self.kwargs.get('pk')
        return CustomUser.objects.filter(pk=business_pk, type='business')


class OrderCompleteCountView(RetrieveAPIView):
    """The view for the endpoint /api/completed-order-count/{business_user_id}/"""
    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the object with the provided id of the business user.
        If the user matching to the given id this returns a 404-error.
        """
        business_pk = self.kwargs.get('pk')
        return CustomUser.objects.filter(pk=business_pk, type='business')
