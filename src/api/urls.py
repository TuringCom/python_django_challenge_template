import logging

from django.urls import path, include
from rest_framework import routers

from api.viewsets.attribute import AttributeViewSet
from api.viewsets.category import CategoryViewSet
from api.viewsets.customers import create_customer, token_obtain_pair, SocialLoginView, update_address, \
    update_credit_card, customer, update_customer
from api.viewsets.department import DepartmentViewSet
from api.viewsets.orders import create_order, order, orders, order_details
from api.viewsets.products import ProductViewSet
from api.viewsets.shipping_region import ShippingRegionViewSet
from api.viewsets.shoppingcart import generate_cart_id, add_products, get_products, update_quantity, empty_cart, \
    remove_product, move_to_cart, total_amount, save_for_later, get_saved_products
from api.viewsets.stripe import charge, webhooks
from api.viewsets.tax import TaxViewSet

logger = logging.getLogger(__name__)

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'tax', TaxViewSet)
router.register(r'shipping/regions', ShippingRegionViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/categories/inProduct/<int:product_id>/', CategoryViewSet.as_view({"get": "get_categories_from_product"})),
    path('v1/categories/inDepartment/<int:department_id>/',
         CategoryViewSet.as_view({"get": "get_categories_from_department"})),
    path('v1/attributes/values/<int:attribute_id>/', AttributeViewSet.as_view({"get": "get_values_from_attribute"})),
    path('v1/attributes/inProduct/<int:product_id>/', AttributeViewSet.as_view({"get": "get_attributes_from_product"})),

    path('v1/products/inCategory/<int:category_id>', ProductViewSet.as_view({"get": "get_products_by_category"})),
    path('v1/products/inDepartment/<int:department_id>', ProductViewSet.as_view({"get": "get_products_by_department"})),

    path('v1/customer', customer),
    path('v1/customer/update', update_customer),

    path('v1/customers', create_customer, name="Create a customer"),
    path('v1/customers/login', token_obtain_pair, name="Create a customer"),
    path('v1/customers/facebook', SocialLoginView.as_view()),
    path('v1/customers/address', update_address),
    path('v1/customers/creditCard', update_credit_card),

    path('v1/orders', create_order),
    path('v1/orders/<int:order_id>', order),
    path('v1/orders/shortDetail/<int:order_id>', order_details),
    path('v1/orders/inCustomer', orders),

    path('v1/shoppingcart/generateUniqueId', generate_cart_id),
    path('v1/shoppingcart/add', add_products),
    path('v1/shoppingcart/<str:cart_id>', get_products),
    path('v1/shoppingcart/update/<int:item_id>', update_quantity),
    path('v1/shoppingcart/empty/<str:cart_id>', empty_cart),
    path('v1/shoppingcart/removeProduct/<int:item_id>', remove_product),
    path('v1/shoppingcart/moveToCart/<int:item_id>', move_to_cart),
    path('v1/shoppingcart/totalAmount/<str:cart_id>', total_amount),
    path('v1/shoppingcart/saveForLater/<int:item_id>', save_for_later),
    path('v1/shoppingcart/getSaved/<str:cart_id>', get_saved_products),

    path('v1/stripe/charge', charge),
    path('v1/stripe/webhooks', webhooks),
]
