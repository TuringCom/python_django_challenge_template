from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from api import errors
from api.models import Customer, Orders, Product, OrderDetail
from api.serializers import OrdersDetailSerializer


class OrdersTests(APITestCase):
    def setUp(self):
        self.url = '/api/v1/orders'

        self.user = User.objects.create_user('test@test.com', 'test@test.com', 'test123**')
        self.customer = Customer.objects.create(user_id=self.user.id, name='Test', email='test@test.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.order = Orders.objects.create(total_amount=50.0, customer_id=self.customer.customer_id)

        self.product = Product.objects.create(
            name="Product Name Test",
            description="Product Desc Test",
            price=25.0,
            discounted_price=5.0
        )

        self.order_detail = OrderDetail.objects.create(
            product_id=self.product.product_id,
            order_id=self.order.order_id,
            attributes='test',
            quantity=1,
            product_name='testProduct',
            unit_cost=25.00
        )

    def test_create_order(self):
        """
        Ensure we can create order
        """

        data = {
            "cart_id": "string",
            "shipping_id": 0,
            "tax_id": 0
        }

        self.assertEqual(Orders.objects.count(), 1)
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Orders.objects.count(), 2)
        assert_data = {'order_id': Orders.objects.count()}
        response_data = json.loads(response.content)
        self.assertEqual(assert_data, response_data)

    def test_create_order_by_invalid_customer(self):
        """
        Ensure we can't create order by anonymous customer
        """
        self.client.logout()
        data = {
            "cart_id": "string",
            "shipping_id": 0,
            "tax_id": 0
        }
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.AUT_02.status)
        self.assertEqual(response_data['error']['code'], errors.AUT_02.code)
        self.assertEqual(response_data['error']['message'], errors.AUT_02.message)

    def test_list_orders_by_customer(self):
        """
        Ensure we can list orders
        """
        url = self.url + '/inCustomer'
        response = self.client.get(url, format='json', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response_data[0]['customer'], self.customer.customer_id)
        self.assertEqual(response_data[0]['order_id'], self.order.order_id)

    def test_retrieve_order(self):
        """
        Ensure we can retrieve order
        """
        url = self.url + '/' + str(self.order.order_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['customer'], self.customer.customer_id)
        self.assertEqual(response_data['order_id'], self.order.order_id)

    def test_detail_order(self):
        """
        Ensure we can get order detail
        """
        url = self.url + '/shortDetail/' + str(self.order.order_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = OrdersDetailSerializer(instance=self.order_detail).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data['order_id'], response_data['order_id'])
        self.assertEqual(serializer_data['name'], response_data['name'])

    def test_detail_with_invalid_order(self):
        """
        Ensure we can get 404 with invalid order id
        """
        url = self.url + '/shortDetail/1000'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.ORD_02.status)
        self.assertEqual(response_data['error']['code'], errors.ORD_02.code)
        self.assertEqual(response_data['error']['message'], errors.ORD_02.message)
