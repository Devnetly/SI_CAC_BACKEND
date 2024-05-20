from rest_framework import serializers
from .models import Immunohistochemistry, Histology, Patient, PatientCollaborator, PatientHistory, Prediction

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

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['primary_doctor']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        else:
            raise serializers.ValidationError(_('User not found in the request'))

        validated_data.pop('primary_doctor', None)  # Remove the 'primary_doctor' field from validated_data

        patient = Patient.objects.create(primary_doctor=user, **validated_data)
        return patient
    
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'