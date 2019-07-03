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
    # TODO: place the code here


@api_view(['POST'])
def webhooks(request):
    """
    Endpoint that provide a synchronization
    """
    # TODO: place the code here
