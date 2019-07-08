from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Department, Category, Attribute, AttributeValue, Product, Customer, Shipping, Tax, ShoppingCart, \
    Orders, OrderDetail, ShippingRegion, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'name', 'description', 'department_id')


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('attribute_value_id', 'value')


class AttributeValueExtendedSerializer(serializers.ModelSerializer):
    attribute_name = serializers.ReadOnlyField(source='attribute.name')
    attribute_value = serializers.ReadOnlyField(source='value')

    class Meta:
        model = AttributeValue
        fields = ('attribute_name', 'attribute_value_id', 'attribute_value')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'description', 'price', 'discounted_price', 'thumbnail')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrdersDetailSerializer(serializers.ModelSerializer):
    total_amount = serializers.ReadOnlyField(source='order.total_amount')
    created_on = serializers.ReadOnlyField(source='order.created_on')
    shipped_on = serializers.ReadOnlyField(source='order.shipped_on')
    status = serializers.ReadOnlyField(source='order.status')
    name = serializers.ReadOnlyField(source='product_name')

    class Meta:
        model = OrderDetail
        fields = ('order_id', 'total_amount', 'created_on', 'shipped_on', 'status', 'name')


class OrdersSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('tax_id', 'shipping_id')


class ShoppingcartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('cart_id', 'attributes', 'product_id', 'quantity')


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('product_id', 'review', 'customer_id', 'rating')


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class ShippingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRegion
        fields = '__all__'


class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'password')


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'password', 'day_phone', 'eve_phone', 'mob_phone')


class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        if hasattr(self.user, 'customer'):
            data['customer'] = CustomerSerializer(self.user.customer).data
        data['access'] = str(refresh.access_token)
        data['expires_in'] = "24h"
        data.pop('refresh')

        return data


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """

    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

    class Meta:
        fields = 'access_token'


class CustomerAddressSerializer(serializers.Serializer):
    address_1 = serializers.CharField(max_length=256, required=True)
    address_2 = serializers.CharField(max_length=256, required=False, allow_null=True)
    city = serializers.CharField(max_length=256, required=True)
    region = serializers.CharField(max_length=256, required=True)
    postal_code = serializers.CharField(max_length=256, required=True)
    country = serializers.CharField(max_length=256, required=True)
    shipping_region_id = serializers.IntegerField(required=True)

    class Meta:
        fields = ('address_1', 'address_2', 'city ', 'region', 'postal_code', 'country', 'shipping_region_id')


class CreditCardSerializer(serializers.Serializer):
    credit_card = serializers.CharField(max_length=256)

    class Meta:
        fields = 'credit_card'
