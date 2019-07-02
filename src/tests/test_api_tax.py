from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Tax
from api.serializers import TaxSerializer


class TaxTests(APITestCase):
    def setUp(self):
        self.url = reverse('tax-list')

        self.tax = Tax.objects.create(tax_type="No Tax", tax_percentage=50.0)

    def test_list_tax(self):
        """
        Ensure we can list tax
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = TaxSerializer(instance=self.tax).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data[0])

    def test_retrieve_tax(self):
        """
        Ensure we can retrieve tax
        """
        url = self.url + str(self.tax.tax_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = TaxSerializer(instance=self.tax).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_not_found_tax(self):
        """
        Ensure we can throw an exception when not found tax
        """
        url = self.url + str(1000) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
