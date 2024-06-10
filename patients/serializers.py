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
    primary_doctor_first_name = serializers.SerializerMethodField()
    primary_doctor_last_name = serializers.SerializerMethodField()
    primary_doctor_profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = '__all__'

    def get_primary_doctor_first_name(self, obj):
        if obj.primary_doctor:
            return obj.primary_doctor.first_name
        return None

    def get_primary_doctor_last_name(self, obj):
        if obj.primary_doctor:
            return obj.primary_doctor.last_name
        return None
    
    def get_primary_doctor_profile_picture(self, obj):
        if obj.primary_doctor and obj.primary_doctor.profile_picture:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.primary_doctor.profile_picture.url)
        return None

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

class MonthlyDiagnosisCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    yes_count = serializers.IntegerField()
    no_count = serializers.IntegerField()


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        count = serializers.IntegerField()
    
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'