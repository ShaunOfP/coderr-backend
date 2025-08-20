from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from userauth_app.models import CustomUser
from .permissions import AllowedToUpdateProfile


class ProfileDetailUpdateView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [AllowedToUpdateProfile()]
        return [IsAuthenticated()]

class BusinessListView(ListAPIView):
    queryset = CustomUser.objects.filter(type='business')
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

class CustomerListView(ListAPIView):
    queryset = CustomUser.objects.filter(type='customer')
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]