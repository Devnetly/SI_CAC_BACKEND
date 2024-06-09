from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()



class Immunohistochemistry(models.Model):
    class Meta:
        verbose_name = _("Immunohistochimie")
        verbose_name_plural = _("Immunohistochimies")


    class HER2Choices(models.TextChoices):
        ONE = '+', _('+')
        TWO = '++', _('++')
        THREE = '+++', _('+++')
    
    class FISHchoices(models.TextChoices):
        POS = '+', _('+')
        NEG = '-', _('-')



    re = models.DecimalField(
        _("RE+"),
        max_digits=5,
        decimal_places=2,blank=False,null=False)
    rp = models.DecimalField(
        _("RP+"),
        max_digits=5,
        decimal_places=2,blank=False,null=False)
    her2 =  models.CharField(
        _("HER2"),
        max_length=3,
        choices=HER2Choices.choices,
        blank=False,null=False
        )
    fish = models.CharField(
        _("HER2"),
        max_length=3,
        choices=FISHchoices.choices,
        blank=True,null=True)
    
    histology_id = models.OneToOneField('Histology', on_delete=models.CASCADE, related_name='immunohistochemistry')





class Histology(models.Model):
    class Meta:
        verbose_name = _("Histologie")
        verbose_name_plural = _("Hostologies")



    class CancerYesNoChoices(models.TextChoices):
        YES = 'Oui', _('Oui')
        NO = 'Non', _('Non')

    class ZoneChoices(models.TextChoices):
        GAUCHE = 'Sein gauche', _('Sein gauche')
        DROIT = 'Sein droit', _('Sein droit')
        AI_GAUCHE = 'Aisselle gauche', _('Aisselle gauche')
        AI_DROIT = 'Aisselle droit', _('Aisselle droit')

    class RankChoices(models.TextChoices):
        ONE = 'I', _('I')
        TWO = 'II', _('II')
        THREE = 'III', _('III')

    class CancerTypeChoices(models.TextChoices):
        ONE = 'Tumeurs épithéliales non infiltrantes', _('Tumeurs épithéliales non infiltrantes')
        TWO = 'Carcinome infiltrant de type non spécifique (canalaire ou NST)', _('Carcinome infiltrant de type non spécifique (canalaire ou NST)')
        THREE = 'Carcinome lobulaire infiltrant', _('Carcinome lobulaire infiltrant')
        FOUR = 'Carcinome tubuleux', _('Carcinome tubuleux')
        FIVE = 'Carcinome cribriforme infiltrant', _('Carcinome cribriforme infiltrant')
        SIX = 'Carcinome médullaire', _('Carcinome médullaire')
        SEVEN = 'Carcinome papillaire infiltrant', _('Carcinome papillaire infiltrant')
        EIGHT = 'Carcinome métaplasique', _('Carcinome métaplasique')
        NINE = 'Carcinome inflammatoire', _('Carcinome inflammatoire')
        TEN = 'Maladie de Paget du mamelon', _('Maladie de Paget du mamelon')

    zone = models.CharField(_("Zone du tissu"),max_length=100,choices=ZoneChoices.choices,blank=False,null=False,unique=True)
    yes_no = models.CharField(_("Cancer ou Pas"),max_length=5,choices=CancerYesNoChoices.choices,blank=False,null=False)
    rank = models.CharField(_("Grade"),max_length=5,choices=RankChoices.choices,blank=False,null=False)
    cancer_type = models.CharField(_("Nature du cancer"),max_length=62,choices=CancerTypeChoices.choices,blank=False,null=False)
    molecular_profile = models.CharField(_("Profil moléculaire"), max_length=150, blank=False,null=False)
    image = models.ImageField(_("Compte rendu"), upload_to='comptes_rendus', blank=True, null=True)
    patient_id = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='histologies')


    

    
    
    
    


class Patient(models.Model):
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


    class GenderChoices(models.TextChoices):
        FEMME = 'FEMME', _('Femme')
        HOMME = 'HOMME', _('Homme')
    class BloodGroupChoices(models.TextChoices):
        A_POSITIVE = 'A+', _('A+')
        A_NEGATIVE = 'A-', _('A-')
        B_POSITIVE = 'B+', _('B+')
        B_NEGATIVE = 'B-', _('B-')
        AB_POSITIVE = 'AB+', _('AB+')
        AB_NEGATIVE = 'AB-', _('AB-')
        O_POSITIVE = 'O+', _('O+')
        O_NEGATIVE = 'O-', _('O-')
    class ExpositionChoices(models.TextChoices):
        RADIATION = 'Radiations Ionisantes', _('Radiation Ionisante')
        PRODUIT = 'Produits Chimiques', _('Produits Chimiques')
        AUTRE = 'Autre', _('Autre')
    class ProgressChoices(models.IntegerChoices):
        ENREGISTRE = 0, _('Enregistré')
        ETAT_CIVIL = 25, _('Etat civil')
        HISTOLOGIE = 50, _('Etude histopathologique')
        IMMUNOMARQUAGE = 75, _('Immunomarquage')
        TERMINER = 100, _('Terminé')

    phone_number_validator = RegexValidator(
        regex=r'^0\d{9}$',
        message=_("Le numéro de téléphone  doit commencer par '0',  et ne contient que 10 chiffres."),
    )
    first_name = models.CharField(_("Prénom"), max_length=150, blank=False,null=False)
    last_name = models.CharField(_("Nom"), max_length=150, blank=False,null=False)
    date_of_birth = models.DateField(_("Date de naissance"),blank=True,null=True)
    place_of_birth = models.CharField(_("Lieu de naissance"), max_length=150, blank=False,null=False,default='')
    gender =  models.CharField(
        _("Sexe"),
        max_length=5,
        choices=GenderChoices.choices,
        blank=False,null=False
        )
    place_of_residence = models.DateField(_("Lieu de résidence"),blank=False,null=False),
    height = models.DecimalField(
        _("Taille"),
        max_digits=5,
        decimal_places=2,validators=[MinValueValidator(0)],blank=False,null=False)
    weight = models.DecimalField(
        _("Poids"),
        max_digits=5,
        decimal_places=2,validators=[MinValueValidator(0)],blank=False,null=False,default=0)
    blood_group = models.CharField(
        _("Group sanguin"),
        max_length=4,
        choices=BloodGroupChoices.choices,
        blank=False,
        null=False,
    )
    profession = models.CharField(_("Proféssion"), max_length=150, blank=False,null=False)
    exposition =  models.CharField(
        _("Exposition"),
        max_length=100,
        choices=ExpositionChoices.choices,
        blank=False,null=False
        )
    other_exposition = models.CharField(_(""), max_length=150, blank=True,null=True)
    phone_number = models.CharField(_("Numéro de téléphone "), max_length=10, blank=True,null=True,validators=[phone_number_validator],)
    primary_doctor = models.ForeignKey(User, verbose_name="Médecin principal", on_delete=models.CASCADE, related_name="primary_patients", null=True, blank=True)
    progress = models.IntegerField(_("Status"), choices=ProgressChoices.choices, default=0)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
       

    def age(self):
        return int((datetime.date.today() - self.date_of_birth) / 365.25  )
    
    def full_name(self):
        return  self.first_name.capitalize() +' '+self.last_name.upper()
    
    
class Prediction(models.Model):
    #bening, malignant, atypical probabilities
    benign = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    malignant = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    atypical = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    histology = models.ForeignKey(Histology, on_delete=models.CASCADE, related_name='predictions')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

class PatientCollaborator(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="collaborators")
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborating_patients")

    class Meta:
        unique_together = ('patient', 'collaborator')


#keep track of patient modifications
class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='history')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_patients')
    modified_at = models.DateTimeField(default=timezone.now)
    data = models.TextField()

    class Meta:
        ordering = ['-modified_at']
