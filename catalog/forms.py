from django import forms
from .models import Product, Category, Contact
from django.core.exceptions import ValidationError
from django.conf import settings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_p', 'price_by', 'description_p', 'picture', 'category']

    def clean_name_p(self, **kwargs ):
        name_p = self.cleaned_data.get('name_p')
        # cleaned_product = Product.objects.get(pk=kwargs['pk'])

        for word in name_p.split():
            if word.lower()  in settings.FORBIDDEN_WORDS:
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите название товара, не использую слова из него.')
        # if Product.objects.filter(name_p=name_p, pk=cleaned_product.pk).exists():
        #     raise ValidationError('Товар с таким названием уже существует.')
        return name_p

    def clean_description_p(self):
        description_p = self.cleaned_data.get('description_p')

        for word in description_p.split():
            if word.lower()  in settings.FORBIDDEN_WORDS:
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите описание товара, не использую слова из него.')
        return description_p

    def clean_price_by(self):
        price_by = self.cleaned_data.get('price_by')

        if price_by <= 0:
            raise ValidationError('Цена товара не может быть отрицательной или равняться 0. Укажите корректную цену товара.')
        return price_by

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
