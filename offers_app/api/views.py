from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny


from offers_app.models import Offer
from .serializers import OfferSerializer
from .permissions import IsUserOfTypeBusiness

class OfferListView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsUserOfTypeBusiness()]