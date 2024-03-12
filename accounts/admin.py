from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import TokenProxy


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmation du mot de passe", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username","email","gender","service"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne sont pas identiques")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        required=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["username","password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["last_name","first_name","username","email","specialty","service","rank"]
    list_filter = []
    fieldsets = [
        (None, {"fields": ["username", "email","is_active" ,"password"]}),
        ("Personal info", {"fields": ["first_name","last_name","date_of_birth","gender","service","specialty","rank"]}),
        ("Permissions", {"fields": ["is_superuser"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["first_name", "last_name", "username", "email","gender","date_of_birth","service","specialty","rank","password1", "password2"],
            },
        ),
    ]
    search_fields = ["last_name","first_name"]
    ordering = ["last_name"]
    list_per_page = 15
    filter_horizontal = []

    def save_model(self, request, obj, form, change):
        # Ensure the password is hashed when saving the user in the admin site
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data["password"])
        obj.save()




admin.site.register(User, UserAdmin)



admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(TokenProxy)






