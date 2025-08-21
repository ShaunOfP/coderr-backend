from django.urls import path

from .views import OrderListCreateView, OrderUpdateDeleteView, OrderCountDetailView, OrderCompleteCountView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderUpdateDeleteView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderCountDetailView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/',
         OrderCompleteCountView.as_view(), name='order-complete')
]
