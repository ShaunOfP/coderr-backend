from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


from offers_app.models import Offer
from .serializers import OfferSerializer
from .permissions import IsUserOfTypeBusiness


class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsUserOfTypeBusiness()]


class OfferDeleteUpdateDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    # serializer_class =
    permission_classes = []


class OfferDetailsDetailView(RetrieveAPIView):
    queryset = Offer.objects.all()
    # serializer_class =
    permission_classes = []
