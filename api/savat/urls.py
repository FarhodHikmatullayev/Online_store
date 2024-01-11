from django.urls import path

from api.savat.views import SavatListAPIView, SavatAddAPIView, SavatDeleteApiView

urlpatterns = [
    path('list/', SavatListAPIView.as_view()),
    path('create/', SavatAddAPIView.as_view()),
    path('delete/<int:pk>/', SavatDeleteApiView.as_view()),
]
