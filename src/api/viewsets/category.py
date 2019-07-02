from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api import errors
from api.models import Category, Product
from api.serializers import CategorySerializer
import logging

logger = logging.getLogger(__name__)


class CategorySetPagination(PageNumberPagination):
    page_size = 20
    page_query_description = 'Inform the page. Starting with 1. Default: 1'
    page_size_query_param = 'limit'
    page_size_query_description = 'Limit per page, Default: 20.'
    max_page_size = 200


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of categories
    retrieve: Return a category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategorySetPagination
    filter_backends = (OrderingFilter,)
    ordering = ('category_id', 'name')
    ordering_fields = ('category_id', 'name')

    @action(detail=False, url_path='inProduct/<int:product_id>')
    def get_categories_from_product(self, request, *args, **kwargs):
        """
        Return a list of categories from a Product ID
        """
        logger.debug("Getting categories from product ID")
        if 'product_id' not in kwargs:
            errors.COM_01.field = 'product_id'
            logger.error("Field product_id is missing")
            return errors.handle(errors.COM_01)
        product_id = int(kwargs['product_id'])

        try:
            # product = Product.objects.get(pk=product_id) TODO: FIX THIS
            categories = Category.objects.filter(prod_categories__product_id=product_id)
            serializer_element = CategorySerializer(categories, many=True)
            logger.debug("Success")
            return Response(serializer_element.data)
        except Product.DoesNotExist:
            logger.error(errors.PRO_01.message)
            return errors.handle(errors.PRO_01)
        except Exception as error:
            logger.error(str(error))
            errors.COM_00.message = str(error)
            return errors.handle(errors.COM_00)

    @action(detail=False, url_path='inDepartment/<int:department_id>')
    def get_categories_from_department(self, request, *args, **kwargs):
        """
        Return a list of categories from a Department ID
        """
        logger.debug("Getting categories from department ID")
        if 'department_id' not in kwargs:
            errors.COM_01.field = 'department_id'
            logger.error("Field department_id is missing")
            return errors.handle(errors.COM_01)
        department_id = int(kwargs['department_id'])
        try:
            categories = Category.objects.filter(department_id=department_id)
            serializer_element = CategorySerializer(categories, many=True)
            logger.debug("Success")
            return Response(serializer_element.data)
        except Exception as error:
            logger.error(str(error))
            errors.COM_00.message = str(error)
            return errors.handle(errors.COM_00)
