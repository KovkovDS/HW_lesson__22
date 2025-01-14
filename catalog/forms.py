from dataclasses import fields

from django import forms
from .models import Product, Category, Contact
from django.core.exceptions import ValidationError
from django.conf import settings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_p', 'price_by', 'hit_sales', 'description_p', 'picture', 'category']

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

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # self.error_class({'class': "text-danger"})
        self.fields['name_p'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название товара'})
        # self.fields('name_p.errors').widget.attrs.update({'class': 'text-danger'})
        self.fields['hit_sales'].widget.attrs.update({'class': 'form-check-input', 'type': 'checkbox'})
        self.fields['price_by'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену товара'})
        self.fields['description_p'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                          'rows': "4",'placeholder': 'Введите описание товара'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile'})
        self.fields['category'].widget.attrs.update({'class': 'form-select form-select-sm', 'aria-label': 'Small select example'})


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
