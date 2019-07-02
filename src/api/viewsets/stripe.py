from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import payments, errors
from api.payments import PaymentError
import logging

logger = logging.getLogger(__name__)


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'stripeToken': openapi.Schema(type=openapi.TYPE_STRING,
                                      description="The API token, you can use this example to get it: https://stripe.com/docs/stripe-js/elements/quickstart",
                                      required=['true']),
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                   description="The order ID recorded before (Check the Order Documentation)",
                                   required=['true']),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description to order.", required=['true']),
        'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description="Only numbers like: 999", required=['true']),
        'currency': openapi.Schema(type=openapi.TYPE_STRING,
                                   description="Check here the options: https://stripe.com/docs/currencies",
                                   default='USD')

    }
))
@api_view(['POST'])
def charge(request):
    """
    This method receive a front-end payment and create a charge.
    """
    logger.debug("Creating a charge")
    stripe_token = request.data.get('stripeToken', None)
    order_id = request.data.get('order_id', None)
    description = request.data.get('description', None)
    amount = request.data.get('amount', None)
    currency = request.data.get('currency', None)

    if stripe_token is None:
        errors.COM_01.field = 'stripe_token'
        logger.error(errors.COM_01.message)
        return errors.handle(errors.COM_01)

    if order_id is None:
        errors.COM_01.field = 'order_id'
        logger.error(errors.COM_01.message)
        return errors.handle(errors.COM_01)

    if description is None:
        errors.COM_01.field = 'description'
        logger.error(errors.COM_01.message)
        return errors.handle(errors.COM_01)

    if amount is None:
        errors.COM_01.field = 'amount'
        logger.error(errors.COM_01.message)
        return errors.handle(errors.COM_01)
    try:
        response = payments.create(amount=amount, order_id=order_id, currency=currency, source=stripe_token,
                                   description=description)
        logger.debug("Success")
        return Response(response)
    except PaymentError as error:
        errors.COM_02.message = error.message
        errors.COM_02._status = error.status
        errors.COM_02.code = error.code
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)


@api_view(['POST'])
def webhooks(request):
    """
    Endpoint that provide a synchronization
    """
    logger.debug("Getting Webhooks")
    try:
        response = payments.create_webhook()
        logger.debug("Success")
        return Response(response)
    except PaymentError as error:
        errors.COM_02.message = error.message
        errors.COM_02._status = error.status
        errors.COM_02.code = error.code
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)
