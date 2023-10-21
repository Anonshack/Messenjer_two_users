from django.db import models


# Create your models here.
class Categories(models.Model):
    category_name_uz = models.CharField(max_length=50, verbose_name='Kategoriya nomi')
    category_name_en = models.CharField(max_length=50, verbose_name='Category name')
    category_name_ru = models.CharField(max_length=50, verbose_name='Imya kategoriya')

    class Meta:
        db_table = 'foods_categories'
        ordering = ['category_name_uz']


class Foods(models.Model):
    food_name_uz = models.CharField(max_length=50, verbose_name='Taom nomi')
    food_name_en = models.CharField(max_length=50, verbose_name='Food name')
    food_name_ru = models.CharField(max_length=50, verbose_name='Imya blyuda')
    food_price = models.IntegerField(verbose_name='Narx/Price (so`m)')
    food_image = models.ImageField(upload_to='foods')
    food_category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        db_table = 'foods_foods'
        ordering = ['food_name_uz']