from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Attribute, Product, AttributeValue, ProductAttribute
from api.serializers import AttributeSerializer


class AttributeTests(APITestCase):
    def setUp(self):
        self.url = reverse('attribute-list')

        self.attribute = Attribute.objects.create(name="color")

        self.attr_value = AttributeValue.objects.create(attribute_id=self.attribute.attribute_id, value="red")

        self.product = Product.objects.create(
            name="Product Name Test",
            description="Product Desc Test",
            price=25.0,
            discounted_price=5.0
        )

        ProductAttribute.objects.create(product_id=self.product.product_id,
                                        attribute_value=self.attr_value)

    def test_list_attributes(self):
        """
        Ensure we can list attributes
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = AttributeSerializer(instance=self.attribute).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data[0])

    def test_retrieve_attributes(self):
        """
        Ensure we can retrieve attributes
        """
        url = self.url + str(self.attribute.attribute_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = AttributeSerializer(instance=self.attribute).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_attributes_by_product(self):
        """
        Ensure we can get attributes by product id
        """
        url = self.url + 'inProduct/' + str(self.product.product_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "attribute_name": self.attribute.name,
            "attribute_value_id": self.attr_value.attribute_value_id,
            "attribute_value": self.attr_value.value
        }]
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(data, response_data)

    def test_get_values_by_attribute(self):
        """
        Ensure we can get values by attribute id
        """
        url = self.url + 'values/' + str(self.attribute.attribute_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "attribute_value_id": self.attr_value.attribute_value_id,
            "value": self.attr_value.value
        }]
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(data, response_data)
