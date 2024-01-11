from rest_framework import serializers

from api.users.serializers import UserSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'user', 'user_id', 'is_active', 'photo', 'price', 'created_time', 'updated_time')

        extra_kwargs = {
            'photo': {
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
