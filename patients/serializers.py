from rest_framework import serializers
from .models import Immunohistochemistry, Histology, Patient, PatientCollaborator, PatientHistory, Prediction
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
User = get_user_model() 

class ImmunochemistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunohistochemistry
        fields = '__all__'

class HistologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Histology
        fields = '__all__'

class PatientCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCollaborator
        fields = ['collaborator']

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_picture')

class PatientSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(source='doctor_id', read_only=True)
    class Meta:
        model = Patient
        fields =  fields = ('id', 'first_name','last_name', 'date_of_birth', 'place_of_birth', 'gender', 'place_of_residence', 'height', 'weight', 'blood_group', 'profession', 'exposition', 'phone_number', 'primary_doctor', 'histologies', 'progress', 'doctor', 'created_at', 'updated_at', 'status', 'archived')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        else:
            raise serializers.ValidationError(_('User not found in the request'))

        validated_data.pop('primary_doctor', None)  # Remove the 'primary_doctor' field from validated_data

        patient = Patient.objects.create(primary_doctor=user, **validated_data)
        return patient
    
    
class PatientCountSerializer(serializers.Serializer):
    all_time = serializers.IntegerField()
    this_year = serializers.IntegerField()
    this_month = serializers.IntegerField()
    this_week = serializers.IntegerField()


class DoctorCountSerializer(serializers.Serializer):
    all_time = serializers.IntegerField()
    this_year = serializers.IntegerField()
    this_month = serializers.IntegerField()
    this_week = serializers.IntegerField()
    

class CancerPatientCountSerializer(serializers.Serializer):
    all_time = serializers.IntegerField()
    this_year = serializers.IntegerField()
    this_month = serializers.IntegerField()
    this_week = serializers.IntegerField()

class MonthlyGenderPatientCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    male_count = serializers.IntegerField()
    female_count = serializers.IntegerField()


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        count = serializers.IntegerField()
    
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'