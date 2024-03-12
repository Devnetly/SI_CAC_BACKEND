from django.db import models
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin,Permission,Group
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import PermissionDenied
from django.apps import apps




class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.TextChoices):
        FEMME = 'FEMME', _('Femme')
        HOMME = 'HOMME', _('Homme')
    class SpecialtyChoices(models.TextChoices):
        CH = 'Ch', _('Chirurgien')
        O = 'O', _('Oncologue')
    class ServiceChoices(models.TextChoices):
        X = 'X', _('x')
        Y = 'Y', _('Y')
    class RankChoices(models.TextChoices):
        X = 'X', _('X')
        Y = 'Y', _('Y')
    first_name = models.CharField(_("Prénom"), max_length=150, blank=False,null=False)
    last_name = models.CharField(_("Nom"), max_length=150, blank=False,null=False)
    date_of_birth = models.DateField(_("Date de naissance"),blank=True,null=True)
    gender =  models.CharField(
        _("Sexe"),
        max_length=5,
        choices=GenderChoices.choices,
        blank=False,null=False
        )
    email = models.EmailField(_("Adresse e-mail"), blank=False,null=False,unique=True)
    specialty = models.CharField(
        _("Specialité"),
        max_length=30,
        choices=SpecialtyChoices.choices,
        blank=False,null=False
        )
    service = models.CharField(
        _("Service"),
        max_length=30,
        choices=ServiceChoices.choices,
        blank=False,null=False
        )
    rank = models.CharField(
        _("Grade"),
        max_length=30,
        choices=ServiceChoices.choices,
        blank=False,null=False
        )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("non d'utilisateur"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        _("compte activé"),
        default=True,)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    profile_picture = models.ImageField(_("photo de profil"),upload_to='profile_pics', blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name","last_name"]

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return  self.first_name.capitalize() +' '+self.last_name.upper()

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)