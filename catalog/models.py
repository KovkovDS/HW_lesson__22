from django.db import models

# Create your models here.

class Category(models.Model):
    name_c = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description_c = models.TextField(null=True, blank=True, verbose_name='Описание')


    def __str__(self):
        return f'{self.name_c}. {self.description_c}.'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name_c']

class Product(models.Model):
    name_p = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description_p = models.TextField(null=True, blank=True, verbose_name='Описание')
    picture = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Категория')
    price_by = models.IntegerField(verbose_name='Цена за покупку')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name_p}. {self.category}. {self.price_by}. {self.updated_at}. {self.description_p}.'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name_p']