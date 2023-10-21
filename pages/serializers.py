from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField

from .models import Categories, Foods


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class FoodsSerializer(ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'


class CategoryFoodsSerializer(Serializer):
    category = CategoriesSerializer(many=True)
    food = FoodsSerializer(many=True)