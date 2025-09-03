from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from userauth_app.models import CustomUser
from .permissions import AllowedToUpdateProfile


class ProfileDetailUpdateView(RetrieveUpdateAPIView):
    """The view for the endpoint /api/profile/{pk}/"""
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """Uses different permissions for different HTTP-Methods"""
        if self.request.method == 'PATCH':
            return [AllowedToUpdateProfile()]
        return [IsAuthenticated()]


class BusinessListView(ListAPIView):
    """
    The view for the endpoint /api/profile/business/.
    Returns a list of all available business users.
    """
    queryset = CustomUser.objects.filter(type='business')
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]


class CustomerListView(ListAPIView):
    """
    The view for the endpoint /api/profile/customer/.
    Returns a list of all available customer users.
    """
    queryset = CustomUser.objects.filter(type='customer')
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
