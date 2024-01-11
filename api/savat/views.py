from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from savat.models import Savat
from api.savat.serializers import SavatSerializer
from shared.pagination import CustomPagination


class SavatListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        savat_projects = Savat.objects.filter(user_id=user.id)
        pagination = CustomPagination()
        page_obj = pagination.paginate_queryset(savat_projects, request)
        serializer = SavatSerializer(page_obj, many=True)
        return pagination.get_paginated_response(data=serializer.data)


class SavatAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = request.user
        quantity = data.get('quantity')
        product_id = data.get('product_id')
        product = get_object_or_404(Product.objects.all(), id=product_id)
        price = product.price * quantity
        data['price'] = price
        data['user_id'] = user.id
        serializer = SavatSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'data': serializer.data,
                'status': status.HTTP_201_CREATED
            }
        )


class SavatDeleteApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        savat = get_object_or_404(Savat.objects.all(), id=pk)
        if not savat.user == user:
            raise ValidationError(
                {
                    'success': False,
                    'detail': 'You are not owner this obj, you are not permission for delete',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
        savat.delete()
        return Response(
            {
                'success': True,
                'detail': 'You deleted your obj successfully'
            }
        )
