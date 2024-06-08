from django.urls import path
from .views import UserProfileDetailView
from .views import TokenObtainPairView




app_name = "accounts"


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),
]  