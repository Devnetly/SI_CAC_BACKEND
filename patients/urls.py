from django.urls import path, include
from rest_framework import routers
from .views import ImmunochemistryViewSet, HistologyViewSet, PatientViewSet, PatientsByDoctorView, PatientCollaboratorViewSet, PatientHistoryView, PredictionViewSet

router = routers.DefaultRouter()
router.register(r'immunochemistries', ImmunochemistryViewSet)
router.register(r'histologies', HistologyViewSet)
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('medics/<int:doctor_id>/', PatientsByDoctorView.as_view(), name='patients-by-doctor'),
    path('<int:patient_id>/history/', PatientHistoryView.as_view(), name='patient-history'),
    path('collaborators/<int:patient_id>/', PatientCollaboratorViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy'
    }), name='patient-collaborators'),
    path('predictions/', PredictionViewSet.as_view({'get': 'list_preds'})),
    path('predictions/<int:patient_id>/', PredictionViewSet.as_view({'post': 'create', 'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]