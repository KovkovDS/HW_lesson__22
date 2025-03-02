from django import forms
from .models import Product, Contact
from django.core.exceptions import ValidationError
from django.conf import settings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_p', 'price_by', 'hit_sales', 'published', 'description_p', 'picture', 'category']

    def clean_name_p(self, **kwargs):
        name_p = self.cleaned_data.get('name_p')
        cleaned_product_pk = self.instance.pk

        for forbidden_word in settings.FORBIDDEN_WORDS:
            if forbidden_word.lower() in name_p.lower():
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите название товара, не использую слова из '
                                      'него.')
        if Product.objects.filter(name_p=name_p).exclude(id=cleaned_product_pk).exists():
            raise ValidationError('Товар с таким названием уже существует.')
        return name_p

    def clean_description_p(self):
        description_p = self.cleaned_data.get('description_p')

        for forbidden_word in settings.FORBIDDEN_WORDS:
            if forbidden_word.lower() in description_p.lower():
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите описание товара, не использую слова из '
                                      'него.')
        return description_p

    def clean_price_by(self):
        price_by = self.cleaned_data.get('price_by')

        if price_by <= 0:
            raise ValidationError('Цена товара не может быть отрицательной или равняться 0. Укажите корректную цену '
                                  'товара.')
        return price_by

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name_p'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название товара'})
        self.fields['hit_sales'].widget.attrs.update({'class': 'form-check-input', 'type': 'checkbox'})
        self.fields['published'].widget.attrs.update({'class': 'form-check-input', 'type': 'checkbox'})
        self.fields['price_by'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену товара'})
        self.fields['description_p'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                          'rows': "4", 'placeholder': 'Введите описание товара'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile'})
        self.fields['category'].widget.attrs.update({'class': 'form-select form-select-sm',
                                                     'aria-label': 'Small select example'})


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
