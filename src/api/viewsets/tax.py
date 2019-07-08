from rest_framework import viewsets

from api.models import Tax
from api.serializers import TaxSerializer
import logging

logger = logging.getLogger(__name__)


class TaxViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Get All Taxes
    retrieve: Get Tax by ID
    """
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
