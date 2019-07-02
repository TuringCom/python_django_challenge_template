from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from api import errors
from api.models import Product, Review, Customer, ProductCategory, Category, Department
from api.serializers import ProductSerializer, ReviewSerializer


class ProductTests(APITestCase):
    def setUp(self):
        self.url = reverse('product-list')

        self.product = Product.objects.create(
            name="Product Name Test",
            description="Product Desc Test",
            price=25.0,
            discounted_price=5.0
        )

        self.department = Department.objects.create(name="Regional")
        self.category = Category.objects.create(name="French", department_id=self.department.department_id)

        ProductCategory.objects.create(product_id=self.product.product_id,
                                       category_id=self.category.category_id)

        self.user = User.objects.create_user('test@test.com', 'test@test.com', 'test123**')
        self.customer = Customer.objects.create(user_id=self.user.id, name='Test', email='test@test.com')
        self.review = Review.objects.create(
            customer_id=self.customer.customer_id,
            product_id=self.product.product_id,
            review="testReview",
            rating=5.0
        )

    def test_list_products(self):
        """
        Ensure we can list products
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data['results'][0])

    def test_retrieve_products(self):
        """
        Ensure we can retrieve products
        """
        url = self.url + str(self.product.product_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_product_reviews(self):
        """
        Ensure we can get products reviews
        """
        url = self.url + str(self.product.product_id) + '/reviews/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ReviewSerializer(instance=self.review).data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(serializer_data, response_data[0])

    def test_create_reviews(self):
        """
        Ensure we can create reviews
        """

        data = {
            "review": "DataReview",
            "rating": 5.0
        }

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        url = self.url + str(self.product.product_id) + '/review/'
        self.assertEqual(Review.objects.count(), 1)
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Review.objects.count(), 2)
        response_data = json.loads(response.content)
        self.assertEqual(data["review"], response_data["review"])
        self.assertEqual(data["rating"], response_data["rating"])

    def test_create_reviews_with_invalid_user(self):
        """
        Ensure we can create reviews
        """

        data = {
            "review": "DataReview",
            "rating": 5.0
        }

        self.client.logout()
        url = self.url + str(self.product.product_id) + '/review/'
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.AUT_02.status)
        self.assertEqual(response_data['error']['code'], errors.AUT_02.code)
        self.assertEqual(response_data['error']['message'], errors.AUT_02.message)

    def test_list_products_by_category(self):
        """
        Ensure we can list products by category
        """
        url = '/api/v1/products/inCategory/' + str(self.category.category_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)
        self.assertEqual(serializer_data, response_data['results'][0])

    def test_list_products_by_department(self):
        """
        Ensure we can list products by department
        """
        url = '/api/v1/products/inDepartment/' + str(self.department.department_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)
        self.assertEqual(serializer_data, response_data['results'][0])

    def test_get_products_details(self):
        """
        Ensure we can get product details
        """
        url = '/api/v1/products/' + str(self.product.product_id) + '/details/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_products_locations(self):
        """
        Ensure we can get product locations
        """
        url = '/api/v1/products/' + str(self.product.product_id) + '/locations/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = {
            "category_id": self.category.category_id,
            "category_name": self.category.name,
            "department_id": self.department.department_id,
            "department_name": self.department.name
        }
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_products_reviews(self):
        """
        Ensure we can get product reviews
        """
        url = '/api/v1/products/' + str(self.product.product_id) + '/reviews/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ReviewSerializer(instance=self.review).data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(serializer_data, response_data[0])
