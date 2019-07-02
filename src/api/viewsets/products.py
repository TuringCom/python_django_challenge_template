import logging

from django.contrib.auth.models import AnonymousUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api import errors
from api.models import Category, Product, Review
from api.serializers import ProductSerializer, ReviewSerializer

logger = logging.getLogger(__name__)


class ProductSetPagination(PageNumberPagination):
    page_size = 20
    page_query_description = 'Inform the page. Starting with 1. Default: 1'
    page_size_query_param = 'limit'
    page_size_query_description = 'Limit per page, Default: 20.'
    max_page_size = 200


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of products
    retrieve: Return a product by ID.
    """
    queryset = Product.objects.all().order_by('product_id')
    serializer_class = ProductSerializer
    pagination_class = ProductSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'description')

    @action(methods=['GET'], detail=False, url_path='search', url_name='Search products')
    def search(self, request, *args, **kwargs):
        """        
        Search products
        """
        return super().list(request, *args, **kwargs)

    def get_products_by_category(self, request, category_id):
        """
        Get a list of Products by Categories
        """
        logger.debug("Getting products by category")
        page = request.GET.get('page', None)
        limit = request.GET.get('limit', None)
        description_length = request.GET.get('description_length', None)

        pagination_class = ProductSetPagination
        paginator = pagination_class()

        queryset = Product.objects.filter(prod_categories__category_id=category_id).order_by('product_id')
        if page is None:
            paginator.page_query_param = page
        if limit is not None:
            paginator.page_size = limit
        if description_length is not None:
            paginator.page_query_description = description_length

        products = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(products, many=True)
        logger.debug("Success")
        return paginator.get_paginated_response(serializer.data)

    def get_products_by_department(self, request, department_id):
        """
        Get a list of Products of Departments
        """
        logger.debug("Getting products by department")
        page = request.GET.get('page', None)
        limit = request.GET.get('limit', None)
        description_length = request.GET.get('description_length', None)

        pagination_class = ProductSetPagination
        paginator = pagination_class()

        queryset = Product.objects.filter(prod_categories__category__department_id=department_id).order_by(
            '-product_id')
        if page is None:
            paginator.page_query_param = page
        if limit is not None:
            paginator.page_size = limit
        if description_length is not None:
            paginator.page_query_description = description_length

        products = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(products, many=True)
        logger.debug("Success")
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='details')
    def details(self, request, pk):
        """
        Get details of a Product
        """
        logger.debug("Getting products detail")
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            logger.error(errors.PRO_01.message)
            return errors.handle(errors.PRO_01)
        serializer_element = ProductSerializer(product)
        logger.debug("Success")
        return Response(serializer_element.data)

    @action(methods=['GET'], detail=True, url_path='locations')
    def locations(self, request, pk):
        """
        Get locations of a Product
        """
        logger.debug("Getting products locations")
        category = Category.objects.filter(prod_categories__product_id=pk).first()
        if category is None:
            errors.COM_10.message = "Location not found"
            errors.COM_10.status = 404
            logger.error(errors.COM_10.message)
            return errors.handle(errors.COM_10)
        logger.debug("Success")
        return Response(
            {
                "category_id": category.category_id,
                "category_name": category.name,
                "department_id": category.department.department_id,
                "department_name": category.department.name
            }
        )

    @action(methods=['GET'], detail=True, url_path='reviews', url_name='List reviews')
    def reviews(self, request, pk):
        """
        Return a list of reviews
        """
        logger.debug("Getting Reviews")
        reviews = Review.objects.filter(product_id=pk)
        serializer_element = ReviewSerializer(reviews, many=True)
        logger.debug("Success")
        return Response(serializer_element.data)

    @swagger_auto_schema(method='POST', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'review': openapi.Schema(type=openapi.TYPE_STRING, description='Review Text of Product', required=['true']),
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating of Product', required=['true']),
        }
    ))
    @action(methods=['POST'], detail=True, url_path='review', url_name='Create review')
    def review(self, request, pk):
        """
        Create a new review
        """
        logger.debug("Creating a review")
        if isinstance(request.user, AnonymousUser):
            logger.error(errors.AUT_02.message)
            return errors.handle(errors.AUT_02)
        request.data['product_id'] = pk
        request.data['customer_id'] = request.user.customer.customer_id
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                review = Review.objects.create(product_id=pk,
                                               review=request.data['review'],
                                               rating=request.data['rating'],
                                               customer_id=request.data['customer_id'])
                serializer_element = ReviewSerializer(review)
                return Response(serializer_element.data)
            else:
                errors.COM_02.message = serializer.errors
                logger.error(errors.COM_02.message)
                return errors.handle(errors.COM_02)
        except Exception as error:
            errors.COM_02.message = str(error)
            logger.error(errors.COM_02.message)
            return errors.handle(
                errors.COM_02)
