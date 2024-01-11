from rest_framework import serializers

from api.users.serializers import UserSerializer
from products.models import Product, CartItem, Cart


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    is_available = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'user', 'user_id', 'is_available', 'image', 'price', 'created_time',
            'updated_time')

        extra_kwargs = {
            'image': {
                'required': False,
            },
            'created_time': {
                'required': False,
                'read_only': True
            },
            'updated_time': {
                'required': False,
                'read_only': True
            }
        }


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('products',)
