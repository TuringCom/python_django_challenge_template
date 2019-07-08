from rest_framework import viewsets

from api.models import Department
from api.serializers import DepartmentSerializer
import logging

logger = logging.getLogger(__name__)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of departments
    retrieve: Return a department by ID.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
