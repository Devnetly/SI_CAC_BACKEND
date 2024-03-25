from rest_framework import serializers
from .models import Immunohistochemistry, Histology, Patient

class ImmunochemistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunohistochemistry
        fields = '__all__'

class HistologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Histology
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'