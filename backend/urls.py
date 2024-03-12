from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from dj_rest_auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="SI pour le CAC de SBA, projet pluridisciplinaire 2CS ESI SBA",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('accounts.urls')),
    path('patients/',include('patients.urls')),

    path('password-reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password-change/',PasswordChangeView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),




    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
