from rest_framework import status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.products.serializers import ProductSerializer, CartSerializer
from products.models import Product, Cart, CartItem
from shared.pagination import CustomPagination


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
        data['user_id'] = request.user.id
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__title', 'name', 'price']

    def get(self, request):
        search_category = request.query_params.get('category')
        search_name = request.query_params.get('name')
        search_price = request.query_params.get('price')
        user = self.request.user
        queryset = Product.objects.all()
        pagination = CustomPagination()
        if search_category:
            queryset = queryset.filter(category__title__icontains=search_category)
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
        if search_price:
            queryset = queryset.filter(price=search_price)
        page_obj = pagination.paginate_queryset(queryset, request)
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

    def delete(self, request, pk):
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


# This is for cart
class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)


class AddToCartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({'success': 'Product added to cart'})


class CheckoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Bu erda xarid jarayoni amalga oshiriladi
        # ...
        # Buyurtma jarayonini boshqacha kodlar bilan to'ldirishingiz mumkin

        # Buyurtma amalga oshirilgandan so'ng savat bo'shlanadi
        cart.cartitem_set.all().delete()

        return Response({'success': 'Order placed successfully'})
