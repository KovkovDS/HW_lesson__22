from django.core.validators import FileExtensionValidator
from django.db import models
from catalog.validators import validate_image_size


class Category(models.Model):
    name_c = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description_c = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        if self.description_c == '':
            return f'\n\n{self.name_c}'
        return f'\n\n{self.name_c} - \n{self.description_c}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name_c']


class Product(models.Model):
    name_p = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description_p = models.TextField(null=True, blank=True, verbose_name='Описание')
    picture = (models.ImageField
               (upload_to='catalog/images', null=True, blank=True, verbose_name='Изображение',
                validators=[validate_image_size,
                            FileExtensionValidator(['jpg', 'png'],
                                                   'Расширение файла « %(extension)s » не допускается. '
                                                   'Разрешенные расширения: %(allowed_extensions)s .',
                                                   'Недопустимое расширение!')]))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price_by = models.IntegerField(verbose_name='Цена за покупку')
    hit_sales = models.BooleanField(default=False, verbose_name='Хит продаж!')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return (f'\n\nНаименование товара: {self.name_p}. \nКатегория товаров: {self.category}.'
                f' \nЦена: {self.price_by}. \nОписание товара: {self.description_p}.')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['updated_at', 'name_p']


class Contact(models.Model):
    legal_address = models.TextField(null=True, blank=True, verbose_name='Юридический адрес')
    mailing_address = models.TextField(null=True, blank=True, verbose_name='Почтовый адрес')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    tel = models.CharField(max_length=50, verbose_name='Телефон')

    def __str__(self):
        return (f'\n\nЮридический адрес: {self.legal_address}\nПочтовый адрес: {self.mailing_address}'
                f'\nE-mail: {self.email}\nТелефон: {self.tel}.')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
