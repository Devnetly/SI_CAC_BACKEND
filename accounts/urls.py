from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserProfileDetailView
from .views import MyTokenObtainPairView




app_name = "accounts"


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),
 

    
  

   
]  