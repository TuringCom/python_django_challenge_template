import os

import stripe

from turing_backend import settings
import logging

logger = logging.getLogger(__name__)


class PaymentError(Exception):
    def __init__(self, message, status=None, _type=None, code=None, param=None):
        self.message = message
        self.status = status
        self.type = _type
        self.code = code
        self.param = param

    def __str__(self):
        return self.message


def handle_error(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            logger.error(err.get('message'))
            raise PaymentError(message=err.get('message'),
                               status=e.http_status,
                               _type=err.get('type'),
                               code=err.get('code'),
                               param=err.get('param'))
        except stripe.error.RateLimitError as e:
            # Too many requests 
            logger.error('Too many requests made to the API too quickly')
            raise PaymentError(message="Too many requests made to the API too quickly", status=e.http_status)
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            logger.error(e.json_body['error']['message'])
            raise PaymentError(message=e.json_body['error']['message'], status=e.http_status, _type=e.json_body['error']['type'])
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            logger.error('Something went wrong!')
            raise PaymentError(message="Invalid API Key", status=e.http_status)
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            logger.error('Network communication with Stripe failed')
            raise PaymentError(message="Network communication with Stripe failed", status=e.http_status)
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            logger.error(e.json_body['error']['message'])
            raise PaymentError(message=e.json_body['error']['message'], status=e.http_status,
                               _type=e.json_body['error']['type'])
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            logger.error('Something went wrong!')
            raise PaymentError(message="There is something wrong", status=500)

    return wrapper


@handle_error
def create(amount, order_id, currency="usd", source="tok_mastercard", description=None):
    stripe.api_key = settings.STRIPE_API_KEY

    response = stripe.Charge.create(
        amount=amount,
        currency=currency,
        source=source,
        description=description,
        metadata={'order_id': order_id}
    )

    return response


@handle_error
def create_webhook():
    stripe.api_key = settings.STRIPE_API_KEY

    response = stripe.WebhookEndpoint.create(
        url=settings.WEBHOOK['url'],
        enabled_events=settings.WEBHOOK['enabled_events']
    )

    return response
