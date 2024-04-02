from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Immunohistochemistry, Histology, Patient, PatientCollaborator, PatientHistory
from .serializers import ImmunochemistrySerializer, HistologySerializer, PatientSerializer, PatientCollaboratorSerializer, PatientHistorySerializer
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

class PatientHistoryView(generics.ListAPIView):
    serializer_class = PatientHistorySerializer

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        return PatientHistory.objects.filter(patient_id=patient_id)

class PatientCollaboratorViewSet(viewsets.ViewSet):
    queryset = PatientCollaborator.objects.all()
    serializer_class = PatientCollaboratorSerializer

    def list(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        if patient.primary_doctor != request.user:
            return Response({'error': 'You are not authorized to view collaborators for this patient.'},
                             status=status.HTTP_403_FORBIDDEN)
        collaborators = PatientCollaborator.objects.filter(patient=patient)
        serializer = self.serializer_class(collaborators, many=True)
        return Response(serializer.data)

    def create(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        if patient.primary_doctor != request.user:
            return Response({'error': 'You are not authorized to add collaborators to this patient.'},
                             status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        if patient.primary_doctor != request.user:
            return Response({'error': 'You are not authorized to modify collaborators for this patient.'},
                             status=status.HTTP_403_FORBIDDEN)
        collaborator = PatientCollaborator.objects.get(patient=patient, collaborator=request.data.get('collaborator'))
        serializer = self.serializer_class(collaborator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        if patient.primary_doctor != request.user:
            return Response({'error': 'You are not authorized to remove collaborators from this patient.'},
                             status=status.HTTP_403_FORBIDDEN)
        collaborator = PatientCollaborator.objects.get(patient=patient, collaborator=request.data.get('collaborator'))
        collaborator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            raise PermissionDenied("You are not authorized to access patients for this doctor.")

        return Patient.objects.filter(doctors=doctor)