# Generated by Django 5.0.3 on 2024-03-06 18:13

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Immunohistochemistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('re', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='RE+')),
                ('rp', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='RP+')),
                ('her2', models.CharField(choices=[('+', '+'), ('++', '++'), ('+++', '+++')], max_length=3, verbose_name='HER2')),
                ('fish', models.CharField(blank=True, choices=[('+', '+'), ('-', '-')], max_length=3, null=True, verbose_name='HER2')),
            ],
            options={
                'verbose_name': 'Immunohistochimie',
                'verbose_name_plural': 'Immunohistochimies',
            },
        ),
        migrations.CreateModel(
            name='Histology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(choices=[('Sein gauche', 'Sein gauche'), ('Sein droit', 'Sein droit'), ('Aisselle gauche', 'Aisselle gauche'), ('Aisselle droit', 'Aisselle droit')], max_length=100, unique=True, verbose_name='Zone du tissu')),
                ('yes_no', models.CharField(choices=[('Oui', 'Oui'), ('Non', 'Non')], max_length=5, verbose_name='Cancer ou Pas')),
                ('rank', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III')], max_length=5, verbose_name='Grade')),
                ('cancer_type', models.CharField(choices=[('Tumeurs épithéliales non infiltrantes', 'Tumeurs épithéliales non infiltrantes'), ('Carcinome infiltrant de type non spécifique (canalaire ou NST)', 'Carcinome infiltrant de type non spécifique (canalaire ou NST)'), ('Carcinome lobulaire infiltrant', 'Carcinome lobulaire infiltrant'), ('Carcinome tubuleux', 'Carcinome tubuleux'), ('Carcinome cribriforme infiltrant', 'Carcinome cribriforme infiltrant'), ('Carcinome médullaire', 'Carcinome médullaire'), ('Carcinome papillaire infiltrant', 'Carcinome papillaire infiltrant'), ('Carcinome métaplasique', 'Carcinome métaplasique'), ('Carcinome inflammatoire', 'Carcinome inflammatoire'), ('Maladie de Paget du mamelon', 'Maladie de Paget du mamelon')], max_length=62, verbose_name='Nature du cancer')),
                ('molecular_profile', models.CharField(max_length=150, verbose_name='Profil moléculaire')),
                ('image', models.ImageField(blank=True, null=True, upload_to='comptes_rendus', verbose_name='Compte rendu')),
                ('immunohistochemistry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patients.immunohistochemistry')),
            ],
            options={
                'verbose_name': 'Histologie',
                'verbose_name_plural': 'Hostologies',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=150, verbose_name='Nom')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('gender', models.CharField(choices=[('FEMME', 'Femme'), ('HOMME', 'Homme')], max_length=5, verbose_name='Sexe')),
                ('height', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Taille')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=4, verbose_name='Group sanguin')),
                ('profession', models.CharField(max_length=150, verbose_name='Proféssion')),
                ('exposition', models.CharField(choices=[('Radiations Ionisantes', 'Radiation Ionisante'), ('Produits Chimiques', 'Produits Chimiques'), ('Autre', 'Autre')], max_length=100, verbose_name='Exposition')),
                ('other_exposition', models.CharField(blank=True, max_length=150, null=True, verbose_name='')),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message="Le numéro de téléphone  doit commencer par '0',  et ne contient que 10 chiffres.", regex='^0\\d{9}$')], verbose_name='Numéro de téléphone ')),
                ('doctors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('histologies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.histology')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
    ]