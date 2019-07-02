from rest_framework import viewsets

from api.models import ShippingRegion
from api.serializers import ShippingRegionSerializer
import logging

logger = logging.getLogger(__name__)


class ShippingRegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Get All ShippingRegions
    retrieve: Get ShippingRegion by ID
    """
    queryset = ShippingRegion.objects.all()
    serializer_class = ShippingRegionSerializer
