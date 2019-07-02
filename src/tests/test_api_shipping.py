from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import ShippingRegion
from api.serializers import ShippingRegionSerializer


class ShippingTests(APITestCase):
    def setUp(self):
        self.url = '/api/v1/shipping/regions/'

        self.shipping_region = ShippingRegion.objects.create(shipping_region='US / Canada')

    def test_list_shipping_region(self):
        """
        Ensure we can list shipping_region
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ShippingRegionSerializer(instance=self.shipping_region).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data[0])

    def test_retrieve_shipping_region(self):
        """
        Ensure we can retrieve shipping_region
        """
        url = self.url + str(self.shipping_region.shipping_region_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ShippingRegionSerializer(instance=self.shipping_region).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_not_found_shipping(self):
        """
        Ensure we can throw an exception when not found shipping_region
        """
        url = self.url + str(1000) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
