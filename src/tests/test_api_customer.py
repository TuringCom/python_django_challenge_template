from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from api import errors
from api.models import Customer, ShippingRegion
from api.serializers import CustomerSerializer


class CustomerTests(APITestCase):
    def setUp(self):
        self.url = '/api/v1/customer'

        self.user = User.objects.create_user('test@test.com', 'test@test.com', 'test123**')
        self.customer = Customer.objects.create(user_id=self.user.id, name='Test', email='test@test.com')
        self.shipping_region = ShippingRegion.objects.create(shipping_region='US / Canada')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_customer(self):
        """
        Ensure we can get current customer
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = CustomerSerializer(instance=self.customer).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_customer_with_invalid_user(self):
        """
        Ensure we can't get current customer with anonymous user
        """
        self.client.logout()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.USR_10.status)
        self.assertEqual(response_data['error']['code'], errors.USR_10.code)
        self.assertEqual(response_data['error']['message'], errors.USR_10.message)

    def test_update_customer(self):
        """
        Ensure we can update current customer
        """
        url = self.url + '/update'
        data = {
            "name": "testUpdated",
            "email": "test_updated@test.com",
            "password": "passUpdated123**",
            "day_phone": "123",
            "eve_phone": "456",
            "mob_phone": "789"
        }
        response = self.client.put(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        self.assertEqual(data['name'], response_data['name'])
        self.assertEqual(data['email'], response_data['email'])
        self.assertEqual(data['day_phone'], response_data['day_phone'])
        self.assertEqual(data['eve_phone'], response_data['eve_phone'])
        self.assertEqual(data['mob_phone'], response_data['mob_phone'])

    def test_update_customer_with_invalid_user(self):
        """
        Ensure we can't update current customer with anonymous user
        """
        self.client.logout()
        url = self.url + '/update'
        data = {
            "name": "testUpdated",
            "email": "test_updated@test.com",
            "password": "passUpdated123**",
            "day_phone": "123",
            "eve_phone": "456",
            "mob_phone": "789"
        }
        response = self.client.put(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.USR_10.status)
        self.assertEqual(response_data['error']['code'], errors.USR_10.code)
        self.assertEqual(response_data['error']['message'], errors.USR_10.message)

    def test_create_customer(self):
        """
        Ensure we can update current customer
        """
        self.url = '/api/v1/customers'
        data = {
            "name": "newCustomer",
            "email": "new.customer@test.com",
            "password": "passCustomer123**",
        }
        self.assertEqual(Customer.objects.count(), 1)
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 2)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['customer']['schema']['name'], data['name'])
        self.assertEqual(response_data['customer']['schema']['email'], data['email'])

    def test_update_customer_address(self):
        """
        Ensure we can update customer address
        """
        self.url = '/api/v1/customers/address'
        self.client.force_authenticate(user=self.user)
        data = {
            "address_1": "test address 1",
            "address_2": "test address 2",
            "city": "La Habana",
            "region": "Caribe",
            "postal_code": "11400",
            "country": "Cuba",
            "shipping_region_id": self.shipping_region.shipping_region_id
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(data['address_1'], response_data['address_1'])
        self.assertEqual(data['address_2'], response_data['address_2'])
        self.assertEqual(data['city'], response_data['city'])
        self.assertEqual(data['postal_code'], response_data['postal_code'])
        self.assertEqual(data['country'], response_data['country'])
        self.assertEqual(data['shipping_region_id'], response_data['shipping_region'])

    def test_update_customer_credit_card(self):
        """
        Ensure we can update customer credit_card
        """
        self.url = '/api/v1/customers/creditCard'
        self.client.force_authenticate(user=self.user)
        data = {
            "credit_card": "4242424242424242"
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(data['credit_card'], response_data['credit_card'])

    def test_update_customer_credit_card_anonymous_user(self):
        """
        Ensure we can update credit_card with anonymous user
        """
        self.url = '/api/v1/customers/creditCard'
        self.client.logout()
        data = {
            "credit_card": "4242424242424242"
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.USR_10.status)
        self.assertEqual(response_data['error']['code'], errors.USR_10.code)
        self.assertEqual(response_data['error']['message'], errors.USR_10.message)

    def test_update_invalid_credit_card(self):
        """
        Ensure we can update invalid credit_card
        """
        self.url = '/api/v1/customers/creditCard'
        self.client.force_authenticate(user=self.user)
        data = {
            "credit_card": "111313134242424242424242"
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.USR_08.status)
        self.assertEqual(response_data['error']['code'], errors.USR_08.code)
        self.assertEqual(response_data['error']['message'], errors.USR_08.message)

    def test_login_customer(self):
        """
        Ensure we can login
        """
        self.url = '/api/v1/customers/login'
        data = {
            "username": "test@test.com",
            "password": "test123**"
        }

        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['customer']['name'], self.customer.name)
        self.assertEqual(response_data['customer']['email'], self.customer.email)

    def test_invalid_login(self):
        """
        Ensure we can't login
        """
        self.url = '/api/v1/customers/login'
        data = {
            "username": "test@test.com",
            "password": "wrongPass"
        }

        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
