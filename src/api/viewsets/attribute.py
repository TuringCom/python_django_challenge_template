from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api import errors
from api.models import Attribute, AttributeValue
from api.serializers import AttributeSerializer, AttributeValueSerializer, AttributeValueExtendedSerializer
import logging

logger = logging.getLogger(__name__)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of attributes
    retrieve: Return a attribute by ID.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    @action(detail=False, url_path='values/<int:attribute_id>')
    def get_values_from_attribute(self, request, *args, **kwargs):
        """
        Get Values Attribute from Attribute ID
        """
        # TODO: place the code here

    @action(detail=False, url_path='inProduct/<int:product_id>')
    def get_attributes_from_product(self, request, *args, **kwargs):
        """
        Get all Attributes with Product ID
        """
        # TODO: place the code here
