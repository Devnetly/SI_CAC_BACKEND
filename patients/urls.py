from django.urls import path, include
from rest_framework import routers
from .views import ImmunochemistryViewSet, HistologyViewSet, PatientViewSet, PatientsByDoctorView

router = routers.DefaultRouter()
router.register(r'immunochemistries', ImmunochemistryViewSet)
router.register(r'histologies', HistologyViewSet)
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('medics/<int:doctor_id>/', PatientsByDoctorView.as_view(), name='patients-by-doctor'),
]