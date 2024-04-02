from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import Patient, PatientHistory
User = get_user_model() 


#signal to create a new PatientHistory instance whenever a Patient instance is saved
@receiver(pre_save, sender=Patient)
def create_patient_history(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_data = model_to_dict(old_instance)
            current_user = instance.primary_doctor
            PatientHistory.objects.create(
                patient=instance,
                modified_by=current_user,
                data=old_data
            )
        except sender.DoesNotExist:
            pass