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
        exclude = ['doctors']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        else:
            raise serializers.ValidationError(_('User not found in the request'))

        validated_data.pop('doctors', None)  # Remove the 'doctors' field from validated_data

        patient = Patient.objects.create(doctors=user, **validated_data)
        return patient