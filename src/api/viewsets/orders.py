from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import errors
from api.models import Orders, OrderDetail
from api.serializers import OrdersSaveSerializer, OrdersSerializer, OrdersDetailSerializer
import logging

from turing_backend import settings

logger = logging.getLogger(__name__)


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'cart_id': openapi.Schema(type=openapi.TYPE_STRING, description='Cart ID.', required=['true']),
        'shipping_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shipping ID.', required=['true']),
        'tax_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tax ID.', required=['true']),
    }
))
@api_view(['POST'])
def create_order(request):
    """
    Create a Order
    """
    # TODO: place the code here


@api_view(['GET'])
def order(request, order_id):
    """
    Get Info about Order
    """
    # TODO: place the code here


@api_view(['GET'])
def order_details(request, order_id):
    """
    Get Info about Order
    """
    logger.debug("Getting detail info")
    # TODO: place the code here


@api_view(['GET'])
def orders(request):
    """
    Get orders by Customer
    """
    # TODO: place the code here


@api_view(['GET'])
def test(request):
    context = {
        'order_id': 12334,
        'username': 'John Doe'
    }
    return render(request, 'notify_order.html', context)
