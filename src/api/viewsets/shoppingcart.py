import uuid

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from api import errors
from api.models import ShoppingCart
from api.serializers import ShoppingcartSerializer, ProductSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def generate_cart_id(request):
    """
    Generate the unique CART ID 
    """
    logger.debug("Generating cart ID")
    return Response({"cart_id": uuid.uuid4()})


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'cart_id': openapi.Schema(type=openapi.TYPE_STRING, description='Cart ID.', required=['true']),
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product ID.', required=['true']),
        'attributes': openapi.Schema(type=openapi.TYPE_STRING, description='Attributes of Product.', required=['true']),
    }
))
@api_view(['POST'])
def add_products(request):
    """
    Add a Product in the cart
    """
    logger.debug("Adding products")
    serializer = ShoppingcartSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        try:
            serializer.validated_data['product_id'] = request.data['product_id']
            shopping_cart = serializer.save()
            serializer_element = ShoppingcartSerializer(shopping_cart)
            logger.debug("Success")
            return Response(serializer_element.data)
        except Exception as error:
            errors.COM_02.message = str(error)
            logger.error(errors.COM_02.message)
            return errors.handle(errors.COM_02)
    else:
        errors.COM_02.message = serializer.errors
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)


@api_view(['GET'])
def get_products(request, cart_id):
    """
    Get List of Products in Shopping Cart
    """
    logger.debug("Getting a list of products")
    try:
        shopping_cart = ShoppingCart.objects.get(cart_id=cart_id)
        serializer_element = ProductSerializer(shopping_cart.product)
        logger.debug("Success")
        return Response(serializer_element.data)
    except ShoppingCart.DoesNotExist:
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@swagger_auto_schema(method='PUT', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Item Quantity.', required=['true'])
    }
))
@api_view(['PUT'])
def update_quantity(request, item_id):
    """
    Update the cart by item
    """
    logger.debug("Updating quantity")
    quantity = request.data.get('quantity', None)
    if quantity is None:
        errors.COM_02.message = "You must provide a quantity param"
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.COM_02)
    try:
        shopping_cart = ShoppingCart.objects.get(item_id=item_id)
        shopping_cart.quantity = quantity
        shopping_cart.save()
        serializer_element = ShoppingcartSerializer(shopping_cart)
        logger.debug("Success")
        return Response(serializer_element.data)
    except ShoppingCart.DoesNotExist:
        errors.SHP_01.message = "Don't exist shoppingCart with this item_id"
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@api_view(['DELETE'])
def empty_cart(request, cart_id):
    """
    Empty cart
    """
    logger.debug("Emptying")
    try:
        shopping_cart = ShoppingCart.objects.get(cart_id=cart_id)
        shopping_cart.delete()
        logger.debug("Success")
        return Response([])
    except ShoppingCart.DoesNotExist:
        logger.warning("Shopping cart doesn't exists")
        return Response([])


@api_view(['DELETE'])
def remove_product(request, item_id):
    """
    Remove a product in the cart
    """
    logger.debug("Removing a product from a car")
    try:
        shopping_cart = ShoppingCart.objects.get(item_id=item_id)
        shopping_cart.delete()
        logger.debug("Success")
        return Response(status=HTTP_200_OK)
    except ShoppingCart.DoesNotExist:
        errors.SHP_01.message = "Don't exist shoppingCart with this item_id"
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@api_view(['GET'])
def move_to_cart(request, item_id):
    """
    Move a product to cart
    """
    logger.debug("Moving a product")
    try:
        shopping_cart = ShoppingCart.objects.get(item_id=item_id)
        shopping_cart.buy_now = 1
        shopping_cart.added_on = timezone.now()
        shopping_cart.save()
        serializer_element = ShoppingcartSerializer(shopping_cart)
        logger.debug("Success")
        return Response(serializer_element.data)
    except ShoppingCart.DoesNotExist:
        errors.SHP_01.message = "Don't exist shoppingCart with this item_id"
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@api_view(['GET'])
def total_amount(request, cart_id):
    """
    Return a total Amount from Cart
    """
    logger.debug("Getting total amount")
    try:
        shopping_cart = ShoppingCart.objects.get(cart_id=cart_id)
        amount = shopping_cart.quantity * (shopping_cart.product.price or shopping_cart.product.discounted_price)
        logger.debug("Success")
        return Response({"total_amount": amount})
    except ShoppingCart.DoesNotExist:
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@api_view(['GET'])
def save_for_later(request, item_id):
    """
    Save a Product for latter
    """
    logger.debug("Saving a product for later")
    try:
        shopping_cart = ShoppingCart.objects.get(item_id=item_id)
        shopping_cart.quantity = 1
        shopping_cart.buy_now = 0
        shopping_cart.save()
        logger.debug("Success")
        return Response(status=HTTP_200_OK)
    except ShoppingCart.DoesNotExist:
        errors.SHP_01.message = "Don't exist shoppingCart with this item_id"
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)


@api_view(['GET'])
def get_saved_products(request, cart_id):
    """
    Get saved Products 
    """
    logger.debug("Getting saved products")
    try:
        shopping_cart = ShoppingCart.objects.get(cart_id=cart_id)
        if shopping_cart.buy_now == 0:
            serializer_element = ProductSerializer(shopping_cart.product)
            logger.debug("Success")
            return Response(serializer_element.data)
        logger.debug("Success")
        return Response([])
    except ShoppingCart.DoesNotExist:
        logger.error(errors.SHP_01.message)
        return errors.handle(errors.SHP_01)
