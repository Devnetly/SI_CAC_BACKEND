# Generated by Django 5.0.3 on 2024-04-02 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_remove_patient_doctors_alter_patienthistory_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='doctors',
        ),
    ]
