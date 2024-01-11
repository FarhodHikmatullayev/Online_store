from rest_framework import serializers

from api.products.serializers import ProductSerializer
from api.users.serializers import UserSerializer
from savat.models import Savat


class SavatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Savat
        fields = ('user', 'product', 'quantity', 'price', 'created_time', 'user_id', 'product_id')
