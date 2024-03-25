from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Immunohistochemistry, Histology, Patient
from .serializers import ImmunochemistrySerializer, HistologySerializer, PatientSerializer

class ImmunochemistryTests(APITestCase):
    def test_create_immunochemistry(self):
        """
        Ensure we can create a new Immunohistochemistry object.
        """
        url = reverse('immunochemistries')  # Update this line
        data = {
            're': 0.5,
            'rp': 0.7,
            'her2': '+',
            'fish': '+'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Immunohistochemistry.objects.count(), 1)
        self.assertEqual(Immunohistochemistry.objects.get().re, 0.5)