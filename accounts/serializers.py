from rest_framework import serializers
from .models import User
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user ID to the response
        data['user_id'] = self.user.id
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name',"gender","service","specialty","rank","profile_picture")






class CustomPasswordResetSerializer (PasswordResetSerializer):
    def get_email_options(self):
        return {
          'html_email_template_name': 'accounts/reset_password_email_message.html',
          
        }