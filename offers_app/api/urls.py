from django.urls import path
from .views import OfferListCreateView, OfferDeleteUpdateDetailView, OfferDetailsDetailView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDeleteUpdateDetailView.as_view(),
         name='offer-detail'),
    path('offerdetails/<int:pk>/',
         OfferDetailsDetailView.as_view(), name='offer-details')
]
