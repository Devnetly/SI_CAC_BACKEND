from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Immunohistochemistry, Histology, Patient
from .serializers import ImmunochemistrySerializer, HistologySerializer, PatientSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class ImmunochemistryViewSet(viewsets.ModelViewSet):
    queryset = Immunohistochemistry.objects.all()
    serializer_class = ImmunochemistrySerializer
    permission_classes = [IsAuthenticated]

class HistologyViewSet(viewsets.ModelViewSet):
    queryset = Histology.objects.all()
    serializer_class = HistologySerializer
    permission_classes = [IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class PatientsByDoctorView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        try:
            doctor = User.objects.get(id=doctor_id)
        except User.DoesNotExist:
            return Patient.objects.none()

        if doctor != self.request.user:
            return Patient.objects.none()

        return Patient.objects.filter(doctors=doctor)