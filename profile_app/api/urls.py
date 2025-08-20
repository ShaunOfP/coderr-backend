from django.urls import path
from .views import ProfileDetailUpdateView, BusinessListView, CustomerListView

urlpatterns = [
    path('<int:pk>/', ProfileDetailUpdateView.as_view(), name="detail-profile"),
    path('business/', BusinessListView.as_view(), name="business-list"),
    path('customer/', CustomerListView.as_view(), name="customer-list")
]
