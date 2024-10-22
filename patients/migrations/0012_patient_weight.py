# Generated by Django 5.0.3 on 2024-06-07 21:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0011_patient_archived"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="weight",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=5,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Poids",
            ),
        ),
    ]
