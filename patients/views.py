from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Immunohistochemistry, Histology, Patient
from .serializers import ImmunochemistrySerializer, HistologySerializer, PatientSerializer

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