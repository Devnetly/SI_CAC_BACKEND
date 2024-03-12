from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserProfileDetailView




app_name = "accounts"


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),
 

    
  

   
]  