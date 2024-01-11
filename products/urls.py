from django.urls import path

from products.views import ProductListView, ProductDetailView, ProductCreateView, ProductEditView, ProductDeleteView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
