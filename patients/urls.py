from django.urls import path, include
from rest_framework import routers
from .views import ImmunochemistryViewSet, HistologyViewSet, PatientViewSet

router = routers.DefaultRouter()
router.register(r'immunochemistries', ImmunochemistryViewSet)
router.register(r'histologies', HistologyViewSet)
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]