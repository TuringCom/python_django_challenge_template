from rest_framework import status
from rest_framework.test import APITestCase


class StripeTests(APITestCase):
    def setUp(self):
        self.url = '/api/v1/stripe/'

    def test_invalid_token_in_charge_stripe(self):
        """
        Test invalid token when an attempt to create a charge
        """
        data = {
            "stripeToken": "TestToken",
            "order_id": 1,
            "description": "This's a test",
            "amount": 20.0,
            "currency": "USD"
        }

        url = self.url + 'charge'
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['message'], "No such token: TestToken")

    def test_invalid_webhook(self):
        """
        Test invalid webhook
        """
        url = self.url + 'webhooks'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['message'], "You already reached the limit of 16 test webhook endpoints.")
