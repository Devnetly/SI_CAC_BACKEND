from rest_framework.generics import RetrieveAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .models import User
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class DoctorDetailView(RetrieveAPIView):
    queryset = User.objects.filter(is_superuser=False)  # Filter out superusers
    serializer_class = UserProfileSerializer
    lookup_field = 'id'  # Use the username as the lookup field



class UserProfileDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        user_profile = User.objects.get(pk=user_id)
        return user_profile








