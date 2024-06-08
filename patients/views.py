from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Immunohistochemistry, Histology, Patient, PatientCollaborator, PatientHistory, Prediction
from .serializers import ImmunochemistrySerializer, HistologySerializer, PatientSerializer, PatientCollaboratorSerializer, PatientHistorySerializer, PredictionSerializer,PatientCountSerializer, DoctorCountSerializer, CancerPatientCountSerializer,MonthlyGenderPatientCountSerializer
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
    queryset = Patient.objects.filter(archived=False)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class PatientHistologiesView(generics.ListAPIView):
    serializer_class = HistologySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        return Histology.objects.filter(patient_id=patient)


# to return the number of all patients by all time, older than a year ...
class PatientCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_year_ago = now - timedelta(days=365)
        one_month_ago = now - timedelta(days=30)
        one_week_ago = now - timedelta(days=7)
        
        all_time_count = Patient.objects.count()
        this_year_count = Patient.objects.filter(created_at__gte=one_year_ago).count()
        this_month_count = Patient.objects.filter(created_at__gte=one_month_ago).count()
        this_week_count = Patient.objects.filter(created_at__gte=one_week_ago).count()
        
        data = {
            "all_time": all_time_count,
            "this_year": this_year_count,
            "this_month": this_month_count,
            "this_week": this_week_count,
        }
        
        serializer = PatientCountSerializer(data=data)
        serializer.is_valid() 
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# to return the number of patients of the authenticated docter by all time, older than a year ...
class MyPatientCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_year_ago = now - timedelta(days=365)
        one_month_ago = now - timedelta(days=30)
        one_week_ago = now - timedelta(days=7)
        
        doctor = request.user

        all_time_count = Patient.objects.filter(primary_doctor=doctor).count()
        this_year_count = Patient.objects.filter(primary_doctor=doctor, created_at__gte=one_year_ago).count()
        this_month_count = Patient.objects.filter(primary_doctor=doctor, created_at__gte=one_month_ago).count()
        this_week_count = Patient.objects.filter(primary_doctor=doctor, created_at__gte=one_week_ago).count()

        data = {
            "all_time": all_time_count,
            "this_year": this_year_count,
            "this_month": this_month_count,
            "this_week": this_week_count,
        }
        serializer = PatientCountSerializer(data=data)
        serializer.is_valid() 
        return Response(serializer.data, status=status.HTTP_200_OK)

 # to return the total number of docter 

class DoctorCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_year_ago = now - timedelta(days=365)
        one_month_ago = now - timedelta(days=30)
        one_week_ago = now - timedelta(days=7)
        
        all_time_count = User.objects.filter(is_superuser=False).count()
        this_year_count = User.objects.filter(is_superuser=False, date_joined__gte=one_year_ago).count()
        this_month_count = User.objects.filter(is_superuser=False, date_joined__gte=one_month_ago).count()
        this_week_count = User.objects.filter(is_superuser=False, date_joined__gte=one_week_ago).count()
        
        data = {
            "all_time": all_time_count,
            "this_year": this_year_count,
            "this_month": this_month_count,
            "this_week": this_week_count,
        }
        
        serializer = DoctorCountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# to return the number of patients diagnosed with cancer
class CancerPatientCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_year_ago = now - timedelta(days=365)
        one_month_ago = now - timedelta(days=30)
        one_week_ago = now - timedelta(days=7)


        cancer_patients = Patient.objects.filter(histologies__yes_no=Histology.CancerYesNoChoices.YES)
        
        
        all_time_count = cancer_patients.count()
        this_year_count = cancer_patients.filter(created_at__gte=one_year_ago).count()
        this_month_count = cancer_patients.filter(created_at__gte=one_month_ago).count()
        this_week_count = cancer_patients.filter(created_at__gte=one_week_ago).count()

        data = {
            "all_time": all_time_count,
            "this_year": this_year_count,
            "this_month": this_month_count,
            "this_week": this_week_count,
        }
        
        serializer = CancerPatientCountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MonthlyGenderPatientCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        male_counts = Patient.objects.filter(gender=Patient.GenderChoices.HOMME)\
            .annotate(month=TruncMonth('created_at'))\
            .values('month')\
            .annotate(count=Count('id'))\
            .order_by('month')

        female_counts = Patient.objects.filter(gender=Patient.GenderChoices.FEMME)\
            .annotate(month=TruncMonth('created_at'))\
            .values('month')\
            .annotate(count=Count('id'))\
            .order_by('month')

        
        results = {}
        for male in male_counts:
            month_str = male['month'].strftime('%Y-%m')
            if month_str not in results:
                results[month_str] = {'month': month_str, 'male_count': 0, 'female_count': 0}
            results[month_str]['male_count'] = male['count']

        for female in female_counts:
            month_str = female['month'].strftime('%Y-%m')
            if month_str not in results:
                results[month_str] = {'month': month_str, 'male_count': 0, 'female_count': 0}
            results[month_str]['female_count'] = female['count']

        
        data = list(results.values())
        serializer = MonthlyGenderPatientCountSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    



class IncompletePatientsFilesView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = self.request.user
        return Patient.objects.filter(primary_doctor=doctor, progress__lt=100)
    

    
   

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

        return Patient.objects.filter(primary_doctor=doctor)
    

class PredictionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]


    def list_preds(self, request):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        print("predictions",predictions)
        return Response(serializer.data)

    def create(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            prediction = serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        predictions = patient.predictions.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def update(self, request, patient_id, prediction_id):
        patient = Patient.objects.get(id=patient_id)
        try:
            prediction = Prediction.objects.get(id=prediction_id, patient=patient)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PredictionSerializer(prediction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, patient_id):
        try:
            prediction = Prediction.objects.get(patient_id=patient_id)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ListArchivedPatientsView(generics.ListAPIView):
    queryset = Patient.objects.filter(archived=True)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
