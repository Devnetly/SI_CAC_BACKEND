# Generated by Django 5.0.3 on 2024-04-02 01:45

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_patient_progress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='primary_doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_patients', to=settings.AUTH_USER_MODEL, verbose_name='Médecin principal'),
        ),
        migrations.CreateModel(
            name='PatientHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', models.JSONField()),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_patients', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='patients.patient')),
            ],
            options={
                'ordering': ['-modified_at'],
            },
        ),
        migrations.CreateModel(
            name='PatientCollaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborating_patients', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='patients.patient')),
            ],
            options={
                'unique_together': {('patient', 'collaborator')},
            },
        ),
    ]
