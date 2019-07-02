from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Category, Department, Product, ProductCategory
from api.serializers import CategorySerializer


class CategoryTests(APITestCase):
    def setUp(self):
        self.url = reverse('category-list')

        self.department = Department.objects.create(name="Regional")

        self.category = Category.objects.create(name="French", department_id=self.department.department_id)

        self.product = Product.objects.create(
            name="Product Name Test",
            description="Product Desc Test",
            price=25.0,
            discounted_price=5.0
        )

        ProductCategory.objects.create(product_id=self.product.product_id,
                                       category_id=self.category.category_id)

    def test_list_categories(self):
        """
        Ensure we can list categories
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = CategorySerializer(instance=self.category).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data['results'][0])

    def test_retrieve_categories(self):
        """
        Ensure we can retrieve categories
        """
        url = self.url + str(self.category.category_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = CategorySerializer(instance=self.category).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_categories_by_department(self):
        """
        Ensure we can get categories by department id
        """
        url = self.url + 'inDepartment/' + str(self.department.department_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "category_id": self.category.category_id,
            "name": self.category.name,
            "description": None,
            "department_id": self.department.department_id
        }]
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(data, response_data)

    def test_get_categories_by_product(self):
        """
        Ensure we can get categories by product id
        """
        url = self.url + 'inProduct/' + str(self.product.product_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "category_id": self.category.category_id,
            "name": self.category.name,
            "description": None,
            "department_id": self.department.department_id
        }]
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(data, response_data)
