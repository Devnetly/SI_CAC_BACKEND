from rest_framework import serializers
from .models import User
from dj_rest_auth.serializers import PasswordResetSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name',"gender","service","specialty","rank","profile_picture")






class CustomPasswordResetSerializer (PasswordResetSerializer):
    def get_email_options(self):
        return {
          'html_email_template_name': 'accounts/reset_password_email_message.html',
          
        }