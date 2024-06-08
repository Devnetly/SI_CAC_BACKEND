from django.urls import path, include
from rest_framework import routers
from .views import ImmunochemistryViewSet, HistologyViewSet, PatientViewSet, PatientsByDoctorView, PatientCollaboratorViewSet, PatientHistoryView, PatientCountView, MyPatientCountView, PredictionViewSet, DoctorCountView,CancerPatientCountView, MonthlyGenderPatientCountView,IncompletePatientsFilesView,ListArchivedPatientsView
from .views import PatientHistologiesView


router = routers.DefaultRouter()
router.register(r'immunochemistries', ImmunochemistryViewSet)
router.register(r'histologies', HistologyViewSet)
router.register(r'patients', PatientViewSet)

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
    path('patients-number/', PatientCountView.as_view(), name='patient-count'),
    path('patients-number-by-doctor/', MyPatientCountView.as_view(), name='patient-count-by-doctor'),
    path('doctors-number/', DoctorCountView.as_view(), name='doctor-count'),
    path('cancer-patients-number/', CancerPatientCountView.as_view(), name='cancer-patients--count'),
    path('monthly-patient-number-by-gender/', MonthlyGenderPatientCountView.as_view(), name='monthly-gender-patient-count'),
    path('incomplete-files/',IncompletePatientsFilesView.as_view(), name='incomplete-patients-files'),
    path('archived-patients/',ListArchivedPatientsView.as_view(), name='archived-patients'),
    path('<int:patient_id>/histologies/', PatientHistologiesView.as_view(), name='patient-histologies'),
]