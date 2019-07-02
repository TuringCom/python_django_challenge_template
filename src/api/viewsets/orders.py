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
# @swagger_auto_schema(method="POST", request_body=OrdersSaveSerializer)
@api_view(['POST'])
def create_order(request):
    """
    Create a Order
    """
    logger.debug("Creating an order")
    if isinstance(request.user, AnonymousUser):
        logger.error(errors.AUT_02.message)
        return errors.handle(errors.AUT_02)
    serializer = OrdersSaveSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        order = serializer.save()
        order.customer_id = request.user.customer.customer_id
        order.save()
        logger.debug("Success")
        try:
            context = {
                'order_id': order.order_id,
                'username': request.user.username
            }
            email_html_message = render_to_string('notify_order.html', context)
            email_plaintext_message = render_to_string('notify_order.txt', context)
            msg = EmailMultiAlternatives(
                "Order confirmation".format(title=settings.APP_NAME),
                email_plaintext_message,
                settings.EMAIL_HOST_USER,
                [request.user.email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            logger.debug("Sending confirmation email")
            msg.send()
            logger.debug("Email sent")
        except Exception as error:
            logger.warning("Unable to send confirmation email")
            logger.error(error)

        return Response({'order_id': order.order_id}, 200)
    else:
        errors.COM_02.message = serializer.errors
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)


@api_view(['GET'])
def order(request, order_id):
    """
    Get Info about Order
    """
    logger.debug("Getting order info")
    if isinstance(request.user, AnonymousUser):
        logger.error(errors.AUT_02.message)
        return errors.handle(errors.AUT_02)

    try:
        order = Orders.objects.get(pk=order_id)
    except Orders.DoesNotExist:
        logger.error(errors.ORD_01.message)
        return errors.handle(errors.ORD_01)
    serializer_element = OrdersSerializer(order)
    logger.debug("Success")
    return Response(serializer_element.data)


@api_view(['GET'])
def order_details(request, order_id):
    """
    Get Info about Order
    """
    logger.debug("Getting detail info")
    if isinstance(request.user, AnonymousUser):
        logger.error(errors.AUT_02.message)
        return errors.handle(errors.AUT_02)

    try:
        order_detail = OrderDetail.objects.get(order_id=order_id)
    except OrderDetail.DoesNotExist:
        logger.error(errors.ORD_02.message)
        return errors.handle(errors.ORD_02)
    serializer_element = OrdersDetailSerializer(order_detail)
    logger.debug("Success")
    return Response(serializer_element.data)


@api_view(['GET'])
def orders(request):
    """
    Get orders by Customer
    """
    logger.debug("Getting orders by customer")
    if isinstance(request.user, AnonymousUser):
        logger.error(errors.AUT_02.message)
        return errors.handle(errors.AUT_02)

    try:
        customer = request.user.customer
        orders = customer.orders
        serializer_element = OrdersSerializer(orders, many=True)
        logger.debug("Success")
        return Response(serializer_element.data)
    except AttributeError:
        errors.COM_02.message = 'You must be logged in'
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)


@api_view(['GET'])
def test(request):
    context = {
        'order_id': 12334,
        'username': 'Jorge Luis'
    }
    return render(request, 'notify_order.html', context)
