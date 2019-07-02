import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api import errors
from api.models import ShoppingCart, Product
from api.serializers import ProductSerializer, ShoppingcartSerializer


class ShoppingCartTests(APITestCase):
    def setUp(self):
        self.url = '/api/v1/shoppingcart/'

        self.product = Product.objects.create(
            name="Product Name Test",
            description="Product Desc Test",
            price=25.0,
            discounted_price=5.0
        )

        self.shoppingCart = ShoppingCart.objects.create(
            cart_id=str(uuid.uuid4())[:8],
            product_id=self.product.product_id,
            attributes="attr_test"
        )

    def test_add_product_shopping_cart(self):
        """
        Ensure we can add product to the shopping cart
        """

        data = {
            "attributes": "attr_test_2",
            "cart_id": "cart_id_test_2",
            "product_id": self.product.product_id,
            "quantity": None
        }
        url = self.url + 'add'
        self.assertEqual(ShoppingCart.objects.count(), 1)
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(ShoppingCart.objects.count(), 2)
        response_data = json.loads(response.content)
        self.assertEqual(data, response_data)

    def test_add_duplicate_shopping_cart_id(self):
        """
        Ensure we can't add duplicated shopping cart ID
        """

        data = {
            "attributes": "attr_test_2",
            "cart_id": self.shoppingCart.cart_id,
            "product_id": self.product.product_id
        }
        url = self.url + 'add'
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_shopping_cart(self):
        """
        Ensure we can remove the shopping cart
        """
        shopping_cart = ShoppingCart.objects.create(
            cart_id=str(uuid.uuid4())[:8],
            product_id=self.product.product_id,
            attributes="attr_test"
        )
        url = self.url + 'empty/' + str(shopping_cart.cart_id)
        self.assertEqual(ShoppingCart.objects.count(), 2)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShoppingCart.objects.count(), 1)

    def test_save_product_for_later(self):
        """
        Ensure we can save products for later
        """
        url = self.url + 'saveForLater/' + str(self.shoppingCart.item_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_saved_product_for_later(self):
        """
        Ensure we get saved products for later
        """
        self.shoppingCart.buy_now = 0
        self.shoppingCart.save()
        url = self.url + 'getSaved/' + self.shoppingCart.cart_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_saved_product_with_invalid_cart_id(self):
        """
        Ensure we get saved product with invalid cart id
        """
        url = self.url + 'getSaved/invalid_cart_id'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_move_to_cart(self):
        """
        Ensure we get move to cart
        """

        url = self.url + 'moveToCart/' + str(self.shoppingCart.item_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ShoppingcartSerializer(instance=self.shoppingCart).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_move_to_cart_with_invalid_item_id(self):
        """
        Ensure we get move to cart with invalid item ID
        """

        url = self.url + 'moveToCart/10000'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['error']['status'], errors.SHP_01.status)
        self.assertEqual(response_data['error']['code'], errors.SHP_01.code)
        self.assertEqual(response_data['error']['message'], errors.SHP_01.message)

    def test_remove_product(self):
        """
        Ensure we can remove product
        """
        shopping_cart = ShoppingCart.objects.create(
            cart_id=str(uuid.uuid4())[:8],
            product_id=self.product.product_id,
            attributes="attr_test"
        )
        url = self.url + 'removeProduct/' + str(shopping_cart.item_id)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_total_amount(self):
        """
        Ensure we can get total amount
        """
        shopping_cart = ShoppingCart.objects.create(
            cart_id=str(uuid.uuid4())[:8],
            product_id=self.product.product_id,
            attributes="attr_test",
            quantity=5
        )
        url = self.url + 'totalAmount/' + shopping_cart.cart_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount'], 125)

    def test_update_shopping_cart(self):
        """
        Ensure we can update shopping cart
        """
        shopping_cart = ShoppingCart.objects.create(
            cart_id=str(uuid.uuid4())[:8],
            product_id=self.product.product_id,
            attributes="attr_test",
            quantity=5
        )
        url = self.url + 'update/' + str(shopping_cart.item_id)
        data = {
            "quantity": 50
        }
        response = self.client.put(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 50)

    def test_get_products_from_shopping_cart(self):
        """
        Ensure we can get products from shopping cart
        """

        url = self.url + self.shoppingCart.cart_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ProductSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)
