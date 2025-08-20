from django.urls import path
from .views import OfferListView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferListView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferListView.as_view(), name='offer-details')
]
