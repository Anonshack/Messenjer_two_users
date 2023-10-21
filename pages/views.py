from collections import namedtuple

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from pages.serializers import CategoryFoodsSerializer
from .models import Categories, Foods

FoodsAndCategories = namedtuple('FoodsAndCategories', ('category', 'food'))


# Create your views here.
class CategoriesAndFoodsListAPIView(ListAPIView):
    serializer_class = CategoryFoodsSerializer

    def list(self, request, *args, **kwargs):
        try:
            lang = request.GET['lang']
        except:
            lang = 'uz'

        all_categories = Categories.objects.all()
        all_foods = Foods.objects.all()

        foods_and_categories = FoodsAndCategories(
            category = all_categories,
            food = all_foods
        )
        serializer = CategoryFoodsSerializer(foods_and_categories)
        return Response(serializer.data)