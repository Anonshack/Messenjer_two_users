from django.urls import path

from .views import CategoriesAndFoodsListAPIView

urlpatterns = [
    path('list', CategoriesAndFoodsListAPIView.as_view()),
]