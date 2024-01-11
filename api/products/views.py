from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.products.serializers import ProductSerializer
from products.models import Product
from shared.pagination import CustomPagination
from shared.permissions import IsOwnerOrReadOnly


# class ProductListCreateAPIView(ListCreateAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     lookup_field = 'pk'
#     pagination_class = CustomPagination
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#
#
# class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsOwnerOrReadOnly,)
#     lookup_field = 'pk'
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user_id = request.user.id
        data['user_id'] = user_id
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'status': status.HTTP_201_CREATED
        })


class ProductUpdateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        data = request.data
        product = get_object_or_404(Product.objects.all(), id=pk)
        if not product.user == request.user:
            raise ValidationError(
                {
                    'success': False,
                    'detail': 'This project is not yours and you are not permission for update',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
        serializer = ProductSerializer(data=data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
        )

    def patch(self, request, pk):
        data = request.data
        product = get_object_or_404(Product.objects.all(), id=pk)
        if not product.user == request.user:
            raise ValidationError(
                {
                    'success': False,
                    'detail': 'This project is not yours and you are not permission for update',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
        serializer = ProductSerializer(data=data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
        )


class ProductListApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = self.request.user
        product = Product.objects.filter(user=user)
        pagination = CustomPagination()
        page_obj = pagination.paginate_queryset(product, request)
        serializer = ProductSerializer(page_obj, many=True)
        return pagination.get_paginated_response(data=serializer.data)


class ProductDetailApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        product = get_object_or_404(Product.objects.all(), id=pk)
        serializer = ProductSerializer(product)
        return Response(
            {
                'success': 'Ok',
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
        )


class ProductDeleteApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product.objects.all(), id=pk)
        if not product.user == user:
            raise ValidationError(
                {
                    'success': False,
                    'detail': 'This project is not yours and you are not permission for delete',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
        product.delete()
        return Response(
            {
                'success': True,
                'detail': 'You successfully deleted you product',
                'status': status.HTTP_200_OK
            }
        )
