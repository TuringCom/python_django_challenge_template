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
        logger.debug("Getting values from attribute ID")
        if 'attribute_id' not in kwargs:
            errors.COM_01.field = 'attribute_id'
            logger.error("Field attribute_id is missing")
            return errors.handle(errors.COM_01)
        attribute_id = int(kwargs['attribute_id'])

        try:
            values = AttributeValue.objects.filter(attribute_id=attribute_id)
            serializer_element = AttributeValueSerializer(values, many=True)
            logger.debug("Success")
            return Response(serializer_element.data)
        except Exception as error:
            errors.COM_00.message = str(error)
            logger.error(str(error))
            return errors.handle(errors.COM_00)

    @action(detail=False, url_path='inProduct/<int:product_id>')
    def get_attributes_from_product(self, request, *args, **kwargs):
        """
        Get all Attributes with Product ID
        """
        logger.debug("Getting attributes from product ID")
        if 'product_id' not in kwargs:
            errors.COM_01.field = 'product_id'
            logger.error("Field product_id is missing")
            return errors.handle(errors.COM_01)
        product_id = int(kwargs['product_id'])
        try:
            values = AttributeValue.objects.filter(product_attribute__product_id=product_id)
            serializer_element = AttributeValueExtendedSerializer(values, many=True)
            logger.debug("Success")
            return Response(serializer_element.data)
        except Exception as error:
            errors.COM_00.message = str(error)
            logger.error(str(error))
            return errors.handle(errors.COM_00)
