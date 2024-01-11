from django.urls import path

from api.products.views import ProductCreateApiView, \
    ProductUpdateApiView, ProductDeleteApiView, ProductDetailApiView, ProductListApiView

urlpatterns = [
    path('create/', ProductCreateApiView.as_view()),
    path('update/<int:pk>/', ProductUpdateApiView.as_view()),
    path('delete/<int:pk>/', ProductDeleteApiView.as_view()),
    path('detail/<int:pk>/', ProductDetailApiView.as_view()),
    path('list/', ProductListApiView.as_view()),
]
