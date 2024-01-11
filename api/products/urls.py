from django.urls import path

from api.products.views import ProductCreateApiView, \
    ProductUpdateApiView, ProductDeleteApiView, ProductDetailApiView, ProductListApiView, CartView, AddToCartView, \
    CheckoutView

urlpatterns = [
    path('create/', ProductCreateApiView.as_view()),
    path('update/<int:pk>/', ProductUpdateApiView.as_view()),
    path('delete/<int:pk>/', ProductDeleteApiView.as_view()),
    path('detail/<int:pk>/', ProductDetailApiView.as_view()),
    path('list/', ProductListApiView.as_view()),

    # for cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
]
